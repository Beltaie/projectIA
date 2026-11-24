from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models.chat import ChatMessage
from schemas.chat import MessageCreate, MessageOut, MessagePage, SessionCreated
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