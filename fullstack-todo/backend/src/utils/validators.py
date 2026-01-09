import re
from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr


class UserValidation:
    """Validation utilities for user-related data."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
        """
        Validate password strength.
        Returns (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit"

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"

        return True, None

    @staticmethod
    def validate_task_title(title: Optional[str]) -> tuple[bool, Optional[str]]:
        """
        Validate task title length (1-100 characters).
        Returns (is_valid, error_message)
        """
        if title is None:
            return False, "Title cannot be empty"

        if len(title) < 1:
            return False, "Title must be at least 1 character long"

        if len(title) > 100:
            return False, "Title must be no more than 100 characters long"

        return True, None

    @staticmethod
    def validate_task_description(description: Optional[str]) -> tuple[bool, Optional[str]]:
        """
        Validate task description length (0-1000 characters).
        Returns (is_valid, error_message)
        """
        if description is None:
            description = ""

        if len(description) > 1000:
            return False, "Description must be no more than 1000 characters long"

        return True, None


class TaskValidation:
    """Validation utilities for task-related data."""

    @staticmethod
    def validate_task_data(title: str, description: Optional[str] = "") -> list[str]:
        """
        Validate task data and return list of error messages.
        Returns empty list if all validations pass.
        """
        errors = []

        # Use the same validation logic as the individual methods to avoid circular dependency
        if title is None:
            errors.append("Title cannot be empty")
        elif len(title) < 1:
            errors.append("Title must be at least 1 character long")
        elif len(title) > 100:
            errors.append("Title must be no more than 100 characters long")

        if description is not None and len(description) > 1000:
            errors.append("Description must be no more than 1000 characters long")

        return errors

    @staticmethod
    def validate_task_title(title: Optional[str]) -> tuple[bool, Optional[str]]:
        """
        Validate task title length (1-100 characters).
        Returns (is_valid, error_message)
        """
        if title is None:
            return False, "Title cannot be empty"

        if len(title) < 1:
            return False, "Title must be at least 1 character long"

        if len(title) > 100:
            return False, "Title must be no more than 100 characters long"

        return True, None

    @staticmethod
    def validate_task_description(description: Optional[str]) -> tuple[bool, Optional[str]]:
        """
        Validate task description length (0-1000 characters).
        Returns (is_valid, error_message)
        """
        if description is None:
            description = ""

        if len(description) > 1000:
            return False, "Description must be no more than 1000 characters long"

        return True, None