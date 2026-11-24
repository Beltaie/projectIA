from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session
from starlette import status

from config.settings import settings
from core.errors import AppError
from db.models import ConversationMessage, ConversationSession
from schemas.session_memory import MessageCreate


class SessionMemoryService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_session(self) -> ConversationSession:
        now = datetime.now(UTC)
        self.purge_expired_sessions(now)

        active_sessions = self.db_session.scalar(
            select(func.count())
            .select_from(ConversationSession)
            .where(ConversationSession.expires_at > now)
        )
        if (
            active_sessions is not None
            and active_sessions >= settings.session_memory_max_sessions
        ):
            raise AppError(
                "The maximum number of active sessions has been reached.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                code="session_limit_reached",
            )

        conversation = ConversationSession(
            id=str(uuid4()),
            created_at=now,
            expires_at=now
            + timedelta(seconds=settings.session_memory_ttl_seconds),
        )
        self.db_session.add(conversation)
        self.db_session.commit()
        return conversation

    def add_message(
        self,
        session_id: str,
        message_data: MessageCreate,
    ) -> ConversationMessage:
        now = datetime.now(UTC)
        self.purge_expired_sessions(now)
        conversation = self._get_active_session(session_id, now)

        message = ConversationMessage(
            session_id=conversation.id,
            role=message_data.role,
            content=message_data.content,
            created_at=now,
        )
        self.db_session.add(message)
        self.db_session.flush()
        conversation.expires_at = now + timedelta(
            seconds=settings.session_memory_ttl_seconds
        )

        excess_message_ids = self.db_session.scalars(
            select(ConversationMessage.id)
            .where(ConversationMessage.session_id == conversation.id)
            .order_by(
                ConversationMessage.created_at.desc(),
                ConversationMessage.id.desc(),
            )
            .offset(settings.session_memory_max_messages)
        ).all()
        if excess_message_ids:
            self.db_session.execute(
                delete(ConversationMessage).where(
                    ConversationMessage.id.in_(excess_message_ids)
                )
            )

        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def get_memory(
        self,
        session_id: str,
    ) -> tuple[ConversationSession, list[ConversationMessage]]:
        now = datetime.now(UTC)
        self.purge_expired_sessions(now)
        conversation = self._get_active_session(session_id, now)
        messages = list(
            self.db_session.scalars(
                select(ConversationMessage)
                .where(ConversationMessage.session_id == conversation.id)
                .order_by(
                    ConversationMessage.created_at.asc(),
                    ConversationMessage.id.asc(),
                )
            ).all()
        )
        return conversation, messages

    def purge_expired_sessions(self, now: datetime | None = None) -> int:
        current_time = now or datetime.now(UTC)
        expired_session_ids = self.db_session.scalars(
            select(ConversationSession.id).where(
                ConversationSession.expires_at <= current_time
            )
        ).all()
        if not expired_session_ids:
            return 0

        self.db_session.execute(
            delete(ConversationMessage).where(
                ConversationMessage.session_id.in_(expired_session_ids)
            )
        )
        self.db_session.execute(
            delete(ConversationSession).where(
                ConversationSession.id.in_(expired_session_ids)
            )
        )
        self.db_session.commit()
        return len(expired_session_ids)

    def _get_active_session(
        self,
        session_id: str,
        now: datetime,
    ) -> ConversationSession:
        conversation = self.db_session.scalar(
            select(ConversationSession).where(
                ConversationSession.id == session_id,
                ConversationSession.expires_at > now,
            )
        )
        if conversation is None:
            raise AppError(
                "Session not found or expired.",
                status_code=status.HTTP_404_NOT_FOUND,
                code="session_not_found",
            )
        return conversation
