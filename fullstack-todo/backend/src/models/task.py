from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, field_validator
from .user import User


class TaskBase(SQLModel):
    """Base model for task with common fields."""
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    @field_validator('title')
    @classmethod
    def validate_title_length(cls, v):
        if len(v) < 1 or len(v) > 100:
            raise ValueError('Title must be between 1 and 100 characters')
        return v

    @field_validator('description')
    @classmethod
    def validate_description_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be no more than 1000 characters')
        return v


class Task(TaskBase, table=True):
    """Task model for the database."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    """Task model for reading task data."""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """Task model for creating a new task."""
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default="", max_length=1000)


class TaskUpdate(SQLModel):
    """Task model for updating task data."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TaskComplete(SQLModel):
    """Task model for marking task as complete/incomplete."""
    completed: bool