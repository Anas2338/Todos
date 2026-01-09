from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from pydantic import BaseModel
from typing import Optional


class PasswordResetToken(SQLModel, table=True):
    """Database model for password reset tokens."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    token: str = Field(unique=True, index=True)
    expires_at: datetime
    used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ForgotPasswordRequest(BaseModel):
    """Request model for forgot password."""
    email: str


class ForgotPasswordResponse(BaseModel):
    """Response model for forgot password request."""
    message: str


class ResetPasswordRequest(BaseModel):
    """Request model for reset password."""
    token: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    """Response model for reset password request."""
    message: str