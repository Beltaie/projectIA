import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionCreated(BaseModel):
    session_id: uuid.UUID
    session_token: str  # shown once: the server keeps only its hash
    expires_at: datetime


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    created_at: datetime


class MessagePage(BaseModel):
    items: list[MessageOut]
    page: int
    size: int
    total: int
