from pydantic import BaseModel
from typing import Optional


class TaskCreateRequest(BaseModel):
    """Request model for creating a task."""
    title: str
    description: Optional[str] = ""


class TaskUpdateRequest(BaseModel):
    """Request model for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None


class TaskCompleteRequest(BaseModel):
    """Request model for marking a task as complete."""
    completed: bool


class TaskResponse(BaseModel):
    """Response model for task operations."""
    id: str
    title: str
    description: Optional[str] = ""
    completed: bool
    user_id: str
    created_at: str
    updated_at: str


class TaskListResponse(BaseModel):
    """Response model for listing tasks."""
    tasks: list[TaskResponse]