from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated, List
from models.task_models import TaskCreateRequest, TaskUpdateRequest, TaskCompleteRequest, TaskResponse, TaskListResponse
from models.task import TaskCreate, TaskUpdate, TaskComplete
from models.user import User
from services.task_service import TaskService
from utils.connection_pool import get_session
from utils.observability import get_logger, create_http_exception
from .middleware import get_current_user_id
from uuid import UUID

task_router = APIRouter()
logger = get_logger(__name__)
task_service = TaskService()


@task_router.post("/api/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_create: TaskCreateRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Create a new task for a user."""
    try:
        # Verify that the authenticated user is the same as the user in the path
        if current_user_id != user_id:
            raise create_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="FORBIDDEN",
                message="Access denied to this user's tasks"
            )

        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Convert request model to service model
        task_create_model = TaskCreate(
            title=task_create.title,
            description=task_create.description
        )

        # Create task via service
        task = task_service.create_task(session, user_uuid, task_create_model)

        # Handle potential None values for created_at and updated_at with fallback to current time
        created_at_value = task.created_at if task.created_at else datetime.utcnow()
        updated_at_value = task.updated_at if task.updated_at else datetime.utcnow()

        # Return response
        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description or "",
            completed=task.completed,
            user_id=str(task.user_id),
            created_at=created_at_value.isoformat(),
            updated_at=updated_at_value.isoformat()
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during task creation: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during task creation"
        )


@task_router.get("/api/{user_id}/tasks", response_model=TaskListResponse)
def get_all_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get all tasks for a user."""
    try:
        # Verify that the authenticated user is the same as the user in the path
        if current_user_id != user_id:
            raise create_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="FORBIDDEN",
                message="Access denied to this user's tasks"
            )

        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Get all tasks for the user via service
        tasks = task_service.get_all_tasks(session, user_uuid)

        # Format responses
        task_responses = []
        for task in tasks:
            # Handle potential None values for created_at and updated_at with fallback to current time
            created_at_value = task.created_at if task.created_at else datetime.utcnow()
            updated_at_value = task.updated_at if task.updated_at else datetime.utcnow()

            created_at_str = created_at_value.isoformat()
            updated_at_str = updated_at_value.isoformat()

            task_responses.append(
                TaskResponse(
                    id=str(task.id),
                    title=task.title,
                    description=task.description or "",
                    completed=task.completed,
                    user_id=str(task.user_id),
                    created_at=created_at_str,
                    updated_at=updated_at_str
                )
            )

        return TaskListResponse(tasks=task_responses)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during getting all tasks: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during getting all tasks"
        )


@task_router.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for a user."""
    try:
        # Verify that the authenticated user is the same as the user in the path
        if current_user_id != user_id:
            raise create_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="FORBIDDEN",
                message="Access denied to this user's tasks"
            )

        # Convert IDs to UUIDs
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)

        # Get task by ID via service
        task = task_service.get_task_by_id(session, task_uuid, user_uuid)

        if not task:
            raise create_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="TASK_NOT_FOUND",
                message="Task with specified ID not found"
            )

        # Handle potential None values for created_at and updated_at with fallback to current time
        created_at_value = task.created_at if task.created_at else datetime.utcnow()
        updated_at_value = task.updated_at if task.updated_at else datetime.utcnow()

        # Return response
        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description or "",
            completed=task.completed,
            user_id=str(task.user_id),
            created_at=created_at_value.isoformat(),
            updated_at=updated_at_value.isoformat()
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during getting task by ID: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during getting task by ID"
        )


@task_router.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdateRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Update a specific task for a user."""
    try:
        # Verify that the authenticated user is the same as the user in the path
        if current_user_id != user_id:
            raise create_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="FORBIDDEN",
                message="Access denied to this user's tasks"
            )

        # Convert IDs to UUIDs
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)

        # Convert request model to service model, handling empty strings
        # Convert empty strings to None for optional fields to pass validation
        title_value = task_update.title if task_update.title != "" else None
        description_value = task_update.description if task_update.description != "" else None

        task_update_model = TaskUpdate(
            title=title_value,
            description=description_value,
            completed=None  # completed field is not part of update request, handle separately
        )

        # Update task via service
        updated_task = task_service.update_task(session, task_uuid, user_uuid, task_update_model)

        if not updated_task:
            raise create_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="TASK_NOT_FOUND",
                message="Task with specified ID not found"
            )

        # Handle potential None values for created_at and updated_at with fallback to current time
        created_at_value = updated_task.created_at if updated_task.created_at else datetime.utcnow()
        updated_at_value = updated_task.updated_at if updated_task.updated_at else datetime.utcnow()

        # Return response
        return TaskResponse(
            id=str(updated_task.id),
            title=updated_task.title,
            description=updated_task.description or "",
            completed=updated_task.completed,
            user_id=str(updated_task.user_id),
            created_at=created_at_value.isoformat(),
            updated_at=updated_at_value.isoformat()
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during updating task: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during updating task"
        )


@task_router.delete("/api/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete a specific task for a user."""
    try:
        # Verify that the authenticated user is the same as the user in the path
        if current_user_id != user_id:
            raise create_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="FORBIDDEN",
                message="Access denied to this user's tasks"
            )

        # Convert IDs to UUIDs
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)

        # Delete task via service
        success = task_service.delete_task(session, task_uuid, user_uuid)

        if not success:
            raise create_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="TASK_NOT_FOUND",
                message="Task with specified ID not found"
            )

        # Return 204 No Content
        return
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during deleting task: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during deleting task"
        )


@task_router.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    user_id: str,
    task_id: str,
    task_complete: TaskCompleteRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Mark a task as complete or incomplete for a user."""
    try:
        # Verify that the authenticated user is the same as the user in the path
        if current_user_id != user_id:
            raise create_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="FORBIDDEN",
                message="Access denied to this user's tasks"
            )

        # Convert IDs to UUIDs
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)

        # Convert request model to service model
        task_complete_model = TaskComplete(
            completed=task_complete.completed
        )

        # Complete task via service
        updated_task = task_service.complete_task(session, task_uuid, user_uuid, task_complete_model)

        if not updated_task:
            raise create_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="TASK_NOT_FOUND",
                message="Task with specified ID not found"
            )

        # Handle potential None values for created_at and updated_at with fallback to current time
        created_at_value = updated_task.created_at if updated_task.created_at else datetime.utcnow()
        updated_at_value = updated_task.updated_at if updated_task.updated_at else datetime.utcnow()

        # Return response
        return TaskResponse(
            id=str(updated_task.id),
            title=updated_task.title,
            description=updated_task.description or "",
            completed=updated_task.completed,
            user_id=str(updated_task.user_id),
            created_at=created_at_value.isoformat(),
            updated_at=updated_at_value.isoformat()
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during completing task: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during completing task"
        )