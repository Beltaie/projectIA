from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import func, select

from config.settings import settings
from core.errors import AppError
from models.chat import ChatMessage, ChatSession
from services.sessions import (
    add_message,
    create_session,
    delete_expired_sessions,
    hash_token,
)


def _count(db, model) -> int:
    return db.scalar(select(func.count()).select_from(model))


def _insert_session(db, expires_at: datetime) -> ChatSession:
    """Insert a session directly: create_session() would purge expired rows."""
    session = ChatSession(token_hash=hash_token("whatever"), expires_at=expires_at)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def test_new_sessions_get_unique_id_and_token(db) -> None:
    first, first_token = create_session(db)
    second, second_token = create_session(db)

    assert first.id != second.id
    assert first_token != second_token
    assert first.token_hash == hash_token(first_token)
    assert first.token_hash != first_token  # only the hash is stored


def test_session_expiration_respects_configured_ttl(db) -> None:
    before = datetime.now(timezone.utc)
    session, _ = create_session(db)
    after = datetime.now(timezone.utc)

    ttl = timedelta(hours=settings.session_ttl_hours)
    assert before + ttl <= session.expires_at <= after + ttl


def test_message_is_stored(db) -> None:
    session, _ = create_session(db)

    message = add_message(db, session, "user", "Hello")

    assert message.id is not None
    assert message.session_id == session.id
    assert (message.role, message.content) == ("user", "Hello")


def test_message_limit_is_enforced(db, monkeypatch) -> None:
    monkeypatch.setattr(settings, "max_messages_per_session", 3)
    session, _ = create_session(db)
    for i in range(3):
        add_message(db, session, "user", f"message {i}")

    with pytest.raises(AppError) as exc_info:
        add_message(db, session, "user", "one too many")

    assert exc_info.value.status_code == 429
    assert exc_info.value.code == "session_limit_reached"
    assert _count(db, ChatMessage) == 3


def test_delete_expired_sessions_keeps_valid_ones(db) -> None:
    now = datetime.now(timezone.utc)
    expired_id = _insert_session(db, now - timedelta(minutes=1)).id
    valid_id = _insert_session(db, now + timedelta(hours=1)).id

    deleted = delete_expired_sessions(db)

    assert deleted == 1
    remaining = db.scalars(select(ChatSession.id)).all()
    assert remaining == [valid_id]
    assert expired_id not in remaining


def test_purging_an_expired_session_deletes_its_messages(db) -> None:
    now = datetime.now(timezone.utc)
    expired = _insert_session(db, now - timedelta(minutes=1))
    valid = _insert_session(db, now + timedelta(hours=1))
    add_message(db, expired, "user", "will disappear")
    add_message(db, expired, "assistant", "me too")
    add_message(db, valid, "user", "stays")

    delete_expired_sessions(db)

    messages = db.scalars(select(ChatMessage)).all()
    assert [m.content for m in messages] == ["stays"]
    assert messages[0].session_id == valid.id


def test_create_session_purges_expired_sessions(db) -> None:
    expired = _insert_session(db, datetime.now(timezone.utc) - timedelta(minutes=1))
    expired_id = expired.id

    create_session(db)

    assert db.get(ChatSession, expired_id) is None
