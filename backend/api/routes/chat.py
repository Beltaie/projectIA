from datetime import datetime
from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.errors import AppError
from database import get_db
from models.chat import ChatMessage, ChatSession
from models.user import User
from schemas.chat import MessageCreate, MessageOut, MessagePage, SessionClaimed, SessionCreated
from services.auth_service import get_current_user
from services.sessions import add_message, create_session, get_valid_session

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/sessions", status_code=201, response_model=SessionCreated)
def create_chat_session(db: Session = Depends(get_db)):
    """Start a guest conversation. No account needed."""
    session, token = create_session(db)
    return SessionCreated(
        session_id=session.id,
        session_token=token,
        expires_at=session.expires_at,
    )


@router.get("/sessions/{session_id}/messages", response_model=MessagePage)
def list_messages(
    session_id: str,
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    x_session_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    """Messages of one session, oldest first. Needs the X-Session-Token header."""
    session = get_valid_session(db, session_id, x_session_token)

    total = db.scalar(
        select(func.count()).select_from(ChatMessage).where(ChatMessage.session_id == session.id)
    )
    items = db.scalars(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.id)
        .offset(page * size)
        .limit(size)
    ).all()
    return MessagePage(items=items, page=page, size=size, total=total or 0)


@router.post("/sessions/{session_id}/messages", status_code=201, response_model=MessageOut)
def post_message(
    session_id: str,
    body: MessageCreate,
    x_session_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    """Store one visitor message. Needs the X-Session-Token header."""
    session = get_valid_session(db, session_id, x_session_token)
    return add_message(db, session, "user", body.content)


# =========================================================================
# SA-29 : Associer une conversation invitée à un compte candidat (Assignée à : EK)
# =========================================================================

@router.post("/sessions/{session_id}/claim", response_model=SessionClaimed)
def claim_chat_session(
    session_id: str,
    x_session_token: str | None = Header(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Associate an anonymous guest chat session to a candidate's registered account.
    Requires authentication (Bearer JWT) and the guest session token (X-Session-Token).
    """
    session = get_valid_session(db, session_id, x_session_token)

    if session.user_id is not None:
        if session.user_id == current_user.id:
            count = db.scalar(select(func.count()).select_from(ChatMessage).where(ChatMessage.session_id == session.id)) or 0
            return SessionClaimed(
                session_id=session.id,
                claimed_by_user_id=current_user.id,
                claimed_at=session.claimed_at or datetime.now(),
                message_count=count,
                status="already_claimed",
            )
        raise AppError("Cette session est déjà associée à un autre utilisateur.", status_code=403, code="session_already_claimed")

    session.user_id = current_user.id
    session.candidate_id = current_user.id
    session.claimed_at = func.now()
    session.last_activity_at = func.now()
    db.commit()
    db.refresh(session)

    count = db.scalar(select(func.count()).select_from(ChatMessage).where(ChatMessage.session_id == session.id)) or 0
    return SessionClaimed(
        session_id=session.id,
        claimed_by_user_id=current_user.id,
        claimed_at=session.claimed_at,
        message_count=count,
        status="claimed",
    )
