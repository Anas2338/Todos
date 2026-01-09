"""
Custom exceptions for the Todo application
"""


class TodoException(Exception):
    """
    Base exception class for the Todo application
    """
    pass


class TaskNotFoundError(TodoException):
    """
    Raised when a task with a specific ID is not found
    """
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class InvalidTaskError(TodoException):
    """
    Raised when a task is invalid (e.g., title too long)
    """
    def __init__(self, message: str):
        super().__init__(message)


class DuplicateTaskError(TodoException):
    """
    Raised when attempting to create a duplicate task
    """
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} already exists")