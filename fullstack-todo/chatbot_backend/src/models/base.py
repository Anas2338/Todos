"""Base model for all SQLModel entities."""

from sqlmodel import SQLModel as _SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SQLModel(_SQLModel):
    """Base class for all SQLModel entities."""
    class Config:
        arbitrary_types_allowed = True


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""
    created_at: datetime
    updated_at: datetime

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = datetime.now()
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = now
        self.updated_at = now


class BaseModelWithValidation(BaseModel):
    """Base model with validation."""
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True