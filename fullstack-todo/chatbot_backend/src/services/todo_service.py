"""Wrapper for Phase II todo service to handle task operations from MCP tools."""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from datetime import datetime
from ..models.chat_session import ChatSession
from ..models.chat_message import ChatMessage
from ..models.tool_invocation import ToolInvocation
from ..core.database import get_session_context
from abc import ABC, abstractmethod


class TodoServiceInterface(ABC):
    """Abstract interface for todo operations."""

    @abstractmethod
    async def create_task(self, user_id: UUID, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new task."""
        pass

    @abstractmethod
    async def list_tasks(self, user_id: UUID, status: str = "all", limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """List tasks for a user."""
        pass

    @abstractmethod
    async def get_task(self, user_id: UUID, task_id: UUID) -> Optional[Dict[str, Any]]:
        """Get a specific task."""
        pass

    @abstractmethod
    async def update_task(self, user_id: UUID, task_id: UUID, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update a task."""
        pass

    @abstractmethod
    async def delete_task(self, user_id: UUID, task_id: UUID) -> bool:
        """Delete a task."""
        pass

    @abstractmethod
    async def set_task_complete(self, user_id: UUID, task_id: UUID, is_completed: bool) -> Optional[Dict[str, Any]]:
        """Set task completion status."""
        pass


class TodoService(TodoServiceInterface):
    """
    Service for handling todo operations that wraps the Phase II domain logic.
    This service acts as a bridge between the MCP tools and the existing Phase II todo functionality.
    """

    def __init__(self):
        """Initialize the todo service with connection to Phase II domain logic."""
        # In a real implementation, this would import and wrap the Phase II todo service
        # For now, we'll simulate the functionality
        pass

    async def create_task(self, user_id: UUID, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task for the user in the database.
        """
        from ..models.task import Task
        from ..core.database import get_session_context
        from sqlmodel import Session
        import logging

        logger = logging.getLogger(__name__)

        try:
            # Create task in the database using autocommit approach
            db_task = Task(
                user_id=user_id,
                title=title,
                description=description or "",
                completed=False
            )

            logger.info(f"Attempting to create task: {title} for user: {user_id}")

            # Use a separate session to ensure proper transaction handling
            with get_session_context() as session:
                session.add(db_task)

                # Explicitly commit the transaction
                session.commit()

                # Refresh to get the generated ID
                session.refresh(db_task)

                # Verify that the task was created successfully
                if not db_task.id:
                    logger.error("Task creation failed: no ID generated")
                    return {
                        "success": False,
                        "error": "Task creation failed: no ID generated"
                    }

                logger.info(f"Task created successfully in database with ID: {db_task.id}")

                # Create response with properly serialized values
                task_response = {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "description": db_task.description,
                    "completed": db_task.completed,
                    "user_id": str(db_task.user_id),
                    "created_at": db_task.created_at.isoformat(),
                    "updated_at": db_task.updated_at.isoformat()
                }

                # Try to also create the task in the main backend to ensure consistency
                try:
                    from .task_integration_service import task_integration_service
                    await task_integration_service.create_task_in_main_backend(
                        user_id=user_id,
                        title=title,
                        description=description
                    )
                except Exception as e:
                    # Log the error but don't fail the operation
                    logger.warning(f"Could not create task in main backend: {str(e)}")

                logger.info(f"Task creation completed successfully with ID: {db_task.id}")
                return {
                    "success": True,
                    "task": task_response
                }

        except Exception as e:
            logger.error(f"Unexpected error in create_task: {str(e)}", exc_info=True)
            # Return error to prevent success message when task creation fails
            return {
                "success": False,
                "error": f"Unexpected error creating task: {str(e)}"
            }

    async def list_tasks(self, user_id: UUID, status: str = "all", limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        List tasks for a user with optional filtering.
        """
        from ..models.task import Task
        from ..core.database import get_session_context
        from sqlmodel import select

        # Query tasks from the database
        with get_session_context() as session:
            # Build query based on status filter
            query = select(Task).where(Task.user_id == user_id)

            if status == "completed":
                query = query.where(Task.completed == True)
            elif status == "pending":
                query = query.where(Task.completed == False)

            # Apply pagination
            query = query.offset(offset).limit(limit)

            db_tasks = session.exec(query).all()

            # Convert database tasks to response format
            tasks = []
            for db_task in db_tasks:
                task = {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "description": db_task.description,
                    "completed": db_task.completed,
                    "user_id": str(db_task.user_id),
                    "created_at": db_task.created_at.isoformat(),
                    "updated_at": db_task.updated_at.isoformat()
                }
                tasks.append(task)

            # Get total count for pagination
            count_query = select(Task).where(Task.user_id == user_id)
            if status == "completed":
                count_query = count_query.where(Task.completed == True)
            elif status == "pending":
                count_query = count_query.where(Task.completed == False)

            total_count = len(session.exec(count_query).all())

            return {
                "success": True,
                "tasks": tasks,
                "total_count": total_count
            }

    async def get_task(self, user_id: UUID, task_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get a specific task by ID.
        """
        from ..models.task import Task
        from ..core.database import get_session_context
        from sqlmodel import select

        # Query the task from the database
        with get_session_context() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return None

            # Return the task in response format
            task = {
                "id": str(db_task.id),
                "title": db_task.title,
                "description": db_task.description,
                "completed": db_task.completed,
                "user_id": str(db_task.user_id),
                "created_at": db_task.created_at.isoformat(),
                "updated_at": db_task.updated_at.isoformat()
            }

            return {
                "success": True,
                "task": task
            }

    async def update_task(self, user_id: UUID, task_id: UUID, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Update a task's properties in the database.
        """
        from ..models.task import Task
        from ..core.database import get_session_context
        from sqlmodel import select
        from datetime import datetime

        # Get the task from the database
        with get_session_context() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return None

            # Update task properties if provided
            if title is not None:
                db_task.title = title
            if description is not None:
                db_task.description = description
            # Update the timestamp
            db_task.updated_at = datetime.now()

            # Commit the changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Return the updated task
            task = {
                "id": str(db_task.id),
                "title": db_task.title,
                "description": db_task.description,
                "completed": db_task.completed,
                "user_id": str(db_task.user_id),
                "created_at": db_task.created_at.isoformat(),
                "updated_at": db_task.updated_at.isoformat()
            }

            return {
                "success": True,
                "task": task
            }

    async def delete_task(self, user_id: UUID, task_id: UUID) -> bool:
        """
        Delete a task by ID from the database.
        """
        from ..models.task import Task
        from ..core.database import get_session_context
        from sqlmodel import select

        # Find the task in the database
        with get_session_context() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return False

            # Delete the task from the database
            session.delete(db_task)
            session.commit()

            return True

    async def set_task_complete(self, user_id: UUID, task_id: UUID, is_completed: bool) -> Optional[Dict[str, Any]]:
        """
        Set the completion status of a task in the database.
        """
        from ..models.task import Task
        from ..core.database import get_session_context
        from sqlmodel import select
        from datetime import datetime

        # Find the task in the database
        with get_session_context() as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return None

            # Update the task completion status
            db_task.completed = is_completed
            db_task.updated_at = datetime.now()

            # Commit the changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Return the updated task
            task = {
                "id": str(db_task.id),
                "title": db_task.title,
                "description": db_task.description,
                "completed": db_task.completed,
                "user_id": str(db_task.user_id),
                "created_at": db_task.created_at.isoformat(),
                "updated_at": db_task.updated_at.isoformat()
            }

            return {
                "success": True,
                "task": task
            }

    async def validate_user_owns_task(self, user_id: UUID, task_id: UUID) -> bool:
        """
        Validate that a user owns a specific task.

        This method would typically call the Phase II domain logic.
        """
        # In a real implementation, this would check if the user owns the task
        # using Phase II's authentication and authorization logic
        # For now, we'll simulate a positive response
        return True

    async def validate_user_owns_session(self, user_id: UUID, session_id: UUID) -> bool:
        """
        Validate that a user owns a specific chat session.

        This method would typically check the database to ensure the session
        belongs to the user.
        """
        # This would query the database to check session ownership
        # For now, we'll return True as a placeholder
        return True


# Global instance of the todo service
todo_service = TodoService()