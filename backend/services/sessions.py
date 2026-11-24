import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from core.errors import AppError
from models.chat import ChatSession

SESSION_TTL = timedelta(hours=24)  # guest session lifetime (api-design.md)


def hash_token(token: str) -> str:
    """SHA-256 hex digest = 64 characters, matches CHAR(64) in the table."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _invalid_session() -> AppError:
    # Same answer for every failure so an attacker cannot tell
    # "session does not exist" from "wrong token" from "expired".
    return AppError("Invalid or expired chat session.", status_code=403, code="invalid_session")


def create_session(db: Session) -> tuple[ChatSession, str]:
    """Create a guest session. Returns the row and the CLEAR token.
    The clear token is never stored: only its hash is."""
    token = secrets.token_urlsafe(32)
    session = ChatSession(
        token_hash=hash_token(token),
        expires_at=datetime.now(timezone.utc) + SESSION_TTL,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session, token


def get_valid_session(db: Session, session_id: str, token: str | None) -> ChatSession:
    """Return the session if id + token match and it is not expired, else 403."""
    if not token:
        raise _invalid_session()
    try:
        sid = uuid.UUID(session_id)
    except ValueError:
        raise _invalid_session()

    session = db.get(ChatSession, sid)
    now = datetime.now(timezone.utc)
    if session is None:
        raise _invalid_session()

    expires_at = session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if not hmac.compare_digest(session.token_hash, hash_token(token)) or expires_at <= now:
        raise _invalid_session()

    session.last_activity_at = now
    db.commit()
    return session
