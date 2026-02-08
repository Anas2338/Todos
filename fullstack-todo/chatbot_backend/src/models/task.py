"""Task model for the chatbot backend (compatible with main backend)."""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class Task(SQLModel, table=True):
    """Task model compatible with main backend schema."""

    __tablename__ = "task"  # Use same table name as main backend

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(nullable=False, description="ID of the user who owns this task")
    title: str = Field(min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(default="", max_length=1000, description="Optional task description")
    completed: bool = Field(default=False, description="Whether the task is completed")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, description="When the task was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, description="When the task was last updated")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure timestamps are set
        now = datetime.utcnow()
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = now
        if not hasattr(self, 'updated_at') or self.updated_at is None:
            self.updated_at = now


class TaskCreate(SQLModel):
    """Schema for creating a new task."""
    title: str
    description: Optional[str] = ""
    user_id: UUID


class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskRead(SQLModel):
    """Schema for reading task data."""
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime