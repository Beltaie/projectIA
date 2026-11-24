from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_database_session
from schemas.session_memory import (
    MessageCreate,
    MessageResponse,
    SessionCreatedResponse,
    SessionMemoryResponse,
)
from services.session_memory_service import SessionMemoryService

router = APIRouter(prefix="/sessions", tags=["Session memory"])


@router.post("", response_model=SessionCreatedResponse, status_code=201)
def create_session(
    db_session: Session = Depends(get_database_session),
) -> SessionCreatedResponse:
    conversation = SessionMemoryService(db_session).create_session()
    return SessionCreatedResponse(
        session_id=UUID(conversation.id),
        expires_at=conversation.expires_at,
    )


@router.post(
    "/{session_id}/messages",
    response_model=MessageResponse,
    status_code=201,
)
def add_message(
    session_id: UUID,
    message_data: MessageCreate,
    db_session: Session = Depends(get_database_session),
) -> MessageResponse:
    message = SessionMemoryService(db_session).add_message(
        str(session_id),
        message_data,
    )
    return MessageResponse.model_validate(message)


@router.get("/{session_id}/messages", response_model=SessionMemoryResponse)
def get_session_memory(
    session_id: UUID,
    db_session: Session = Depends(get_database_session),
) -> SessionMemoryResponse:
    conversation, messages = SessionMemoryService(db_session).get_memory(
        str(session_id)
    )
    return SessionMemoryResponse(
        session_id=UUID(conversation.id),
        expires_at=conversation.expires_at,
        messages=messages,
    )
