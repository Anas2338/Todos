from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UserSignupRequest(BaseModel):
    """Request model for user signup."""
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')

        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in v):
            raise ValueError('Password must contain at least one special character')

        return v


class UserSignupResponse(BaseModel):
    """Response model for user signup."""
    id: str
    email: EmailStr
    created_at: str


class UserSigninRequest(BaseModel):
    """Request model for user signin."""
    email: EmailStr
    password: str


class UserSigninResponse(BaseModel):
    """Response model for user signin."""
    access_token: str
    token_type: str
    user_id: str