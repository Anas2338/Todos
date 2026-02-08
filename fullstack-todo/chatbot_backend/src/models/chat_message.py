"""Chat message model definition."""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from enum import Enum
from .base import SQLModel as BaseSQLModel, TimestampMixin


class MessageRole(str, Enum):
    """Enumeration for message roles."""
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseSQLModel, TimestampMixin, table=True):
    """Represents individual messages in a conversation between user and assistant."""

    __tablename__ = "chat_messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="chat_sessions.id", nullable=False, description="Foreign key linking to ChatSession")
    role: MessageRole = Field(nullable=False, description="Message role ('user' or 'assistant')")
    content: str = Field(nullable=False, description="The actual message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the message was sent/received")
    message_metadata: Optional[str] = Field(default=None, description="Additional metadata (token counts, etc.) as JSON string")

    # Relationship
    session: "ChatSession" = Relationship(back_populates="messages")

    # Validation rules
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure created_at and updated_at are set
        now = datetime.now()
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = now
        self.updated_at = now

        # Validate role
        if self.role not in [MessageRole.USER, MessageRole.ASSISTANT]:
            raise ValueError("role must be either 'user' or 'assistant'")

        # Validate content is not empty
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("content must not be empty")


class ChatMessageCreate(SQLModel):
    """Schema for creating a new chat message."""
    session_id: UUID
    role: MessageRole
    content: str
    message_metadata: Optional[Dict[str, Any]] = {}


class ChatMessageUpdate(SQLModel):
    """Schema for updating a chat message."""
    content: Optional[str] = None
    message_metadata: Optional[Dict[str, Any]] = None