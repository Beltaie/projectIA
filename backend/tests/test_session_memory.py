from collections.abc import Iterator
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from config.settings import settings
from db.database import get_database_session
from db.models import Base, ConversationMessage, ConversationSession
from main import create_app


@pytest.fixture
def memory_client() -> Iterator[tuple[TestClient, sessionmaker[Session]]]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session_factory = sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )

    def override_database_session() -> Iterator[Session]:
        with test_session_factory() as db_session:
            yield db_session

    app = create_app()
    app.dependency_overrides[get_database_session] = override_database_session
    client = TestClient(app)
    yield client, test_session_factory
    client.close()
    app.dependency_overrides.clear()
    engine.dispose()


def test_session_memory_is_isolated_and_keeps_only_recent_messages(
    memory_client: tuple[TestClient, sessionmaker[Session]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, _ = memory_client
    monkeypatch.setattr(settings, "session_memory_max_messages", 2)

    first_session_id = client.post("/sessions").json()["session_id"]
    second_session_id = client.post("/sessions").json()["session_id"]
    for role, content in (
        ("user", "question 1"),
        ("assistant", "answer 1"),
        ("user", "question 2"),
    ):
        response = client.post(
            f"/sessions/{first_session_id}/messages",
            json={"role": role, "content": content},
        )
        assert response.status_code == 201
    client.post(
        f"/sessions/{second_session_id}/messages",
        json={"role": "user", "content": "other conversation"},
    )

    first_memory = client.get(f"/sessions/{first_session_id}/messages").json()
    second_memory = client.get(f"/sessions/{second_session_id}/messages").json()

    assert [message["content"] for message in first_memory["messages"]] == [
        "answer 1",
        "question 2",
    ]
    assert [message["content"] for message in second_memory["messages"]] == [
        "other conversation"
    ]


def test_expired_session_is_inaccessible_and_its_messages_are_deleted(
    memory_client: tuple[TestClient, sessionmaker[Session]],
) -> None:
    client, test_session_factory = memory_client
    session_id = client.post("/sessions").json()["session_id"]
    client.post(
        f"/sessions/{session_id}/messages",
        json={"role": "user", "content": "temporary data"},
    )
    with test_session_factory() as db_session:
        conversation = db_session.get(ConversationSession, session_id)
        assert conversation is not None
        conversation.expires_at = datetime.now(UTC) - timedelta(seconds=1)
        db_session.commit()

    response = client.get(f"/sessions/{session_id}/messages")

    assert response.status_code == 404
    with test_session_factory() as db_session:
        session_count = db_session.scalar(
            select(func.count()).select_from(ConversationSession)
        )
        message_count = db_session.scalar(
            select(func.count()).select_from(ConversationMessage)
        )
        assert session_count == 0
        assert message_count == 0


def test_session_count_and_message_size_are_bounded(
    memory_client: tuple[TestClient, sessionmaker[Session]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, _ = memory_client
    monkeypatch.setattr(settings, "session_memory_max_sessions", 1)

    first_response = client.post("/sessions")
    second_response = client.post("/sessions")
    message_response = client.post(
        f"/sessions/{first_response.json()['session_id']}/messages",
        json={"role": "user", "content": "x" * 4001},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 429
    assert second_response.json()["error"]["code"] == "session_limit_reached"
    assert message_response.status_code == 422
    assert message_response.json()["error"]["code"] == "validation_error"


def test_empty_message_is_rejected(
    memory_client: tuple[TestClient, sessionmaker[Session]],
) -> None:
    client, _ = memory_client
    session_id = client.post("/sessions").json()["session_id"]

    response = client.post(
        f"/sessions/{session_id}/messages",
        json={"role": "user", "content": "   "},
    )

    assert response.status_code == 422
