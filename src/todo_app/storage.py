"""
In-memory storage manager for the Todo application
"""
from typing import Dict, List, Optional
from .models import Task
from .exceptions import TaskNotFoundError, InvalidTaskError


class TodoStorage:
    """
    In-memory storage manager that handles task operations using a dictionary
    with sequential numeric IDs as keys.
    """

    def __init__(self):
        """
        Initialize the storage with an empty task dictionary and next ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with a unique sequential ID.

        Args:
            title (str): Task title (1-100 characters)
            description (str): Task description (0-500 characters)

        Returns:
            Task: The newly created task with assigned ID
        """
        # Create task with the next available ID
        new_task = Task(self._next_id, title, description)
        self._tasks[self._next_id] = new_task

        # Increment the next ID for the subsequent task
        self._next_id += 1

        return new_task

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The requested task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the storage.

        Returns:
            List[Task]: List of all tasks, sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """
        Update an existing task's title and/or description.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title (if provided)
            description (str, optional): New description (if provided)

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        task = self._tasks[task_id]

        # Update title if provided
        if title is not None:
            if not 1 <= len(title) <= 100:
                raise InvalidTaskError(f"Title must be between 1 and 100 characters, got {len(title)} characters")
            task.title = title

        # Update description if provided
        if description is not None:
            if len(description) > 500:
                raise InvalidTaskError(f"Description must be 500 characters or less, got {len(description)} characters")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was successfully deleted, False if it didn't exist

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
        return True

    def mark_task_complete(self, task_id: int) -> Task:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        task = self._tasks[task_id]
        task.completed = True
        return task

    def mark_task_incomplete(self, task_id: int) -> Task:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        task = self._tasks[task_id]
        task.completed = False
        return task

    def has_tasks(self) -> bool:
        """
        Check if there are any tasks in storage.

        Returns:
            bool: True if there are tasks, False otherwise
        """
        return len(self._tasks) > 0