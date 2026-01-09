"""
Task data model for the Todo application
"""
from datetime import datetime
from typing import Optional


class Task:
    """
    Represents a todo task with an ID, title, description, completion status, and creation timestamp.
    """

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task (sequential, starting from 1)
            title (str): Task title (max 100 characters)
            description (str): Task description (max 500 characters)
            completed (bool): Completion status (default: False)
        """
        if not 1 <= len(title) <= 100:
            raise ValueError(f"Title must be between 1 and 100 characters, got {len(title)} characters")

        if len(description) > 500:
            raise ValueError(f"Description must be 500 characters or less, got {len(description)} characters")

        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()

    def __str__(self):
        """
        String representation of the task for display purposes.
        """
        status_indicator = "[✓]" if self.completed else "[ ]"
        return f"{self.id}. {status_indicator} {self.title} - {self.description}"

    def __repr__(self):
        """
        Developer representation of the task.
        """
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"

    def to_dict(self):
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }