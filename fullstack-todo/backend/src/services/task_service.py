from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from models.task import Task, TaskCreate, TaskUpdate, TaskComplete
from models.user import User
from utils.validators import TaskValidation
from utils.observability import get_logger
from fastapi import HTTPException, status


class TaskService:
    """Service class for task-related operations."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def create_task(self, session: Session, user_id: UUID, task_create: TaskCreate) -> Task:
        """Create a new task for a user."""
        # Validate task data
        validation_errors = TaskValidation.validate_task_data(
            task_create.title,
            task_create.description
        )

        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error_code": "VALIDATION_ERROR",
                    "message": "Validation failed",
                    "details": {"errors": validation_errors}
                }
            )

        # Create new task
        current_time = datetime.utcnow()
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed if hasattr(task_create, 'completed') else False,
            created_at=current_time,
            updated_at=current_time,
            user_id=user_id
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        self.logger.info(f"Created new task with ID: {db_task.id} for user: {user_id}")
        return db_task

    def create_tasks_in_transaction(self, session: Session, user_id: UUID, tasks_create: list[TaskCreate]) -> list[Task]:
        """Create multiple tasks in a single database transaction."""
        created_tasks = []

        try:
            for task_create in tasks_create:
                # Validate task data
                validation_errors = TaskValidation.validate_task_data(
                    task_create.title,
                    task_create.description
                )

                if validation_errors:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail={
                            "error_code": "VALIDATION_ERROR",
                            "message": "Validation failed",
                            "details": {"errors": validation_errors}
                        }
                    )

                # Create new task
                current_time = datetime.utcnow()
                db_task = Task(
                    title=task_create.title,
                    description=task_create.description,
                    completed=task_create.completed if hasattr(task_create, 'completed') else False,
                    created_at=current_time,
                    updated_at=current_time,
                    user_id=user_id
                )

                session.add(db_task)
                created_tasks.append(db_task)

            # Commit all tasks in a single transaction
            session.commit()

            # Refresh each task to get the updated values
            for task in created_tasks:
                session.refresh(task)

            self.logger.info(f"Created {len(created_tasks)} tasks for user: {user_id} in a single transaction")
            return created_tasks

        except Exception as e:
            # Rollback the transaction in case of error
            session.rollback()
            self.logger.error(f"Error during transaction for creating tasks: {str(e)}")
            raise

    def get_task_by_id(self, session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Get a task by its ID for a specific user."""
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        return task

    def get_all_tasks(self, session: Session, user_id: UUID) -> List[Task]:
        """Get all tasks for a specific user."""
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()

        return tasks

    def update_task(self, session: Session, task_id: UUID, user_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task for a specific user."""
        task = self.get_task_by_id(session, task_id, user_id)

        if not task:
            return None

        # Update task fields if provided
        if task_update.title is not None:
            # Validate title
            is_valid, error_msg = TaskValidation.validate_task_title(task_update.title)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={"error_code": "VALIDATION_ERROR", "message": error_msg}
                )
            task.title = task_update.title

        if task_update.description is not None:
            # Validate description
            is_valid, error_msg = TaskValidation.validate_task_description(task_update.description)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={"error_code": "VALIDATION_ERROR", "message": error_msg}
                )
            task.description = task_update.description

        if task_update.completed is not None:
            task.completed = task_update.completed

        # Update the timestamp - ensure it's a proper datetime
        task.updated_at = datetime.utcnow()

        try:
            session.add(task)
            session.commit()
            session.refresh(task)
        except Exception as e:
            session.rollback()
            self.logger.error(f"Database error during task update: {str(e)}")
            raise

        self.logger.info(f"Updated task with ID: {task.id}")
        return task

    def delete_task(self, session: Session, task_id: UUID, user_id: UUID) -> bool:
        """Delete a task for a specific user."""
        task = self.get_task_by_id(session, task_id, user_id)

        if not task:
            return False

        session.delete(task)
        session.commit()

        self.logger.info(f"Deleted task with ID: {task.id}")
        return True

    def complete_task(self, session: Session, task_id: UUID, user_id: UUID, task_complete: TaskComplete) -> Optional[Task]:
        """Mark a task as complete or incomplete for a specific user."""
        task = self.get_task_by_id(session, task_id, user_id)

        if not task:
            return None

        task.completed = task_complete.completed
        task.updated_at = datetime.utcnow()  # Update the timestamp

        session.add(task)
        session.commit()
        session.refresh(task)

        self.logger.info(f"Updated completion status for task with ID: {task.id}")
        return task