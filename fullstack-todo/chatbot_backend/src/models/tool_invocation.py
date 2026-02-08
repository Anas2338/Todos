"""Tool invocation model definition."""

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from enum import Enum
from .base import SQLModel as BaseSQLModel, TimestampMixin


class InvocationStatus(str, Enum):
    """Enumeration for invocation statuses."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


class ToolInvocation(BaseSQLModel, TimestampMixin, table=True):
    """Represents calls made to MCP tools, including arguments, results, and execution context."""

    __tablename__ = "tool_invocations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="chat_sessions.id", nullable=False, description="Foreign key linking to ChatSession")
    tool_name: str = Field(nullable=False, description="Name of the MCP tool invoked")
    arguments: str = Field(default='{}', description="Arguments passed to the tool as JSON string")
    result: Optional[str] = Field(default=None, description="Result returned by the tool as JSON string")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the tool was invoked")
    status: InvocationStatus = Field(nullable=False, description="Status of the invocation ('success', 'error', 'pending')")

    # Relationship
    session: "ChatSession" = Relationship(back_populates="tool_invocations")

    # Validation rules
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure created_at and updated_at are set
        now = datetime.now()
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = now
        self.updated_at = now

        # Validate tool_name is one of the defined MCP tools
        valid_tool_names = [
            "create_task", "list_tasks", "get_task",
            "update_task", "delete_task", "set_task_complete"
        ]
        if self.tool_name not in valid_tool_names:
            raise ValueError(f"tool_name must be one of {valid_tool_names}")

        # Validate status is allowed
        if self.status not in [InvocationStatus.SUCCESS, InvocationStatus.ERROR, InvocationStatus.PENDING]:
            raise ValueError("status must be 'success', 'error', or 'pending'")


class ToolInvocationCreate(SQLModel):
    """Schema for creating a new tool invocation."""
    session_id: UUID
    tool_name: str
    arguments: Dict[str, Any] = {}
    result: Optional[Dict[str, Any]] = None
    status: InvocationStatus


class ToolInvocationUpdate(SQLModel):
    """Schema for updating a tool invocation."""
    result: Optional[Dict[str, Any]] = None
    status: Optional[InvocationStatus] = None