from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints


class MessageCreate(BaseModel):
    role: Literal["user", "assistant"]
    content: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=4000,
        ),
    ]


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: UUID
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime


class SessionCreatedResponse(BaseModel):
    session_id: UUID
    expires_at: datetime


class SessionMemoryResponse(BaseModel):
    session_id: UUID
    expires_at: datetime
    messages: list[MessageResponse]
