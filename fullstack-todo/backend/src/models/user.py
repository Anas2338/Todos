from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from pydantic import BaseModel, field_validator
from pydantic.networks import EmailStr


class UserBase(SQLModel):
    """Base model for user with common fields."""
    email: str = Field(unique=True, nullable=False, max_length=255)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v):
        if '@' not in v or '.' not in v.split('@')[1]:
            raise ValueError('Invalid email format')
        return v


class User(UserBase, table=True):
    """User model for the database."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False, max_length=255)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserRead(UserBase):
    """User model for reading user data."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(SQLModel):
    """User model for creating a new user."""
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @classmethod
    def from_orm(cls, user: User):
        """Create a UserCreate instance from a User ORM object."""
        return cls(
            email=user.email,
            password=""
        )


class UserUpdate(SQLModel):
    """User model for updating user data."""
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=125)


class UserLogin(SQLModel):
    """User model for login requests."""
    email: EmailStr
    password: str