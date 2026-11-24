from datetime import datetime, timedelta, timezone

from config.settings import settings
from models.chat import ChatSession
from services.sessions import hash_token


def _start_session(client) -> tuple[str, dict[str, str]]:
    response = client.post("/api/chat/sessions")
    assert response.status_code == 201
    body = response.json()
    return body["session_id"], {"X-Session-Token": body["session_token"]}


def test_post_session_returns_id_token_and_expiry(client) -> None:
    response = client.post("/api/chat/sessions")

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"session_id", "session_token", "expires_at"}
    expires_at = datetime.fromisoformat(body["expires_at"].replace("Z", "+00:00"))
    ttl = timedelta(hours=settings.session_ttl_hours)
    assert abs(expires_at - (datetime.now(timezone.utc) + ttl)) < timedelta(minutes=1)


def test_post_message_then_list_it(client) -> None:
    session_id, headers = _start_session(client)

    posted = client.post(
        f"/api/chat/sessions/{session_id}/messages",
        json={"content": "  Hello  "},
        headers=headers,
    )
    listed = client.get(f"/api/chat/sessions/{session_id}/messages", headers=headers)

    assert posted.status_code == 201
    assert posted.json()["content"] == "Hello"  # whitespace stripped
    assert listed.status_code == 200
    assert listed.json()["total"] == 1
    assert listed.json()["items"][0]["role"] == "user"


def test_empty_message_is_rejected(client) -> None:
    session_id, headers = _start_session(client)

    for content in ("", "   "):
        response = client.post(
            f"/api/chat/sessions/{session_id}/messages",
            json={"content": content},
            headers=headers,
        )
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "validation_error"


def test_message_over_max_length_is_rejected(client) -> None:
    session_id, headers = _start_session(client)
    url = f"/api/chat/sessions/{session_id}/messages"

    too_long = client.post(
        url, json={"content": "a" * (settings.max_message_length + 1)}, headers=headers
    )
    at_limit = client.post(
        url, json={"content": "a" * settings.max_message_length}, headers=headers
    )

    assert too_long.status_code == 422
    assert too_long.json()["error"]["code"] == "validation_error"
    assert at_limit.status_code == 201


def test_message_limit_returns_429(client, monkeypatch) -> None:
    monkeypatch.setattr(settings, "max_messages_per_session", 2)
    session_id, headers = _start_session(client)
    url = f"/api/chat/sessions/{session_id}/messages"
    for _ in range(2):
        assert client.post(url, json={"content": "hi"}, headers=headers).status_code == 201

    response = client.post(url, json={"content": "hi again"}, headers=headers)

    assert response.status_code == 429
    assert response.json()["error"]["code"] == "session_limit_reached"


def test_expired_session_is_rejected(client, db) -> None:
    import uuid
    session_id, headers = _start_session(client)
    session = db.get(ChatSession, uuid.UUID(session_id))
    session.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    db.commit()

    response = client.post(
        f"/api/chat/sessions/{session_id}/messages",
        json={"content": "hello?"},
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "invalid_session"


def test_missing_or_wrong_token_is_rejected(client) -> None:
    session_id, _ = _start_session(client)
    url = f"/api/chat/sessions/{session_id}/messages"

    no_token = client.get(url)
    wrong_token = client.get(url, headers={"X-Session-Token": "nope"})

    assert no_token.status_code == wrong_token.status_code == 403
    assert no_token.json()["error"]["code"] == "invalid_session"
