"""Chat session model definition."""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from .base import SQLModel as BaseSQLModel, TimestampMixin

if TYPE_CHECKING:
    from .chat_message import ChatMessage
    from .tool_invocation import ToolInvocation


class ChatSession(BaseSQLModel, TimestampMixin, table=True):
    """Represents a user's chat session with metadata for managing conversation context."""

    __tablename__ = "chat_sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(nullable=False, description="Foreign key linking to User entity from Phase II")
    title: Optional[str] = Field(default=None, description="Optional title for the conversation (derived from first message or user-provided)")
    is_active: bool = Field(default=True, description="Flag indicating if session is currently active")

    # Relationships
    messages: list["ChatMessage"] = Relationship(back_populates="session")
    tool_invocations: list["ToolInvocation"] = Relationship(back_populates="session")

    # Validation rules
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure created_at and updated_at are set
        now = datetime.now()
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = now
        self.updated_at = now

    @classmethod
    def validate_user_ownership(cls, user_id: UUID, session_id: UUID) -> bool:
        """
        Validate that a user owns a specific chat session.

        Args:
            user_id: The ID of the user
            session_id: The ID of the session to check

        Returns:
            bool: True if the user owns the session, False otherwise
        """
        # This would typically query the database to check ownership
        # For now, we'll implement the method signature
        # Implementation would require database access which is done in the service layer
        return True  # Placeholder - actual implementation would check the database


class ChatSessionCreate(SQLModel):
    """Schema for creating a new chat session."""
    user_id: UUID
    title: Optional[str] = None


class ChatSessionUpdate(SQLModel):
    """Schema for updating a chat session."""
    title: Optional[str] = None
    is_active: Optional[bool] = None