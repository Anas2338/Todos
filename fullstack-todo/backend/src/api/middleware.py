from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from utils.security import verify_token
from utils.observability import create_http_exception
from models.user import User
from sqlmodel import Session, select
from utils.connection_pool import get_session
from uuid import UUID


class JWTBearer(HTTPBearer):
    """JWT Bearer token authentication middleware."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)

        if credentials:
            if not credentials.scheme or credentials.scheme.lower() != "bearer":
                raise create_http_exception(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    error_code="INVALID_TOKEN",
                    message="Invalid authentication scheme"
                )

            token = credentials.credentials
            return self.verify_jwt(token)
        else:
            raise create_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code="INVALID_TOKEN",
                message="Invalid or missing token"
            )

    def verify_jwt(self, token: str):
        """Verify the JWT token and return the payload if valid."""
        payload = verify_token(token)
        if payload:
            return payload
        else:
            raise create_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code="INVALID_TOKEN",
                message="Invalid or expired token"
            )


def get_current_user_id(request: Request) -> str:
    """Get the current user ID from the JWT token in the request."""
    # Extract the token from the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise create_http_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message="Authentication required"
        )

    token = auth_header[7:]  # Remove "Bearer " prefix
    payload = verify_token(token)

    if not payload:
        raise create_http_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_TOKEN",
            message="Invalid or expired token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise create_http_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_TOKEN",
            message="Invalid token: no user ID"
        )

    return user_id


def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """Verify that the authenticated user owns the resource."""
    return user_id == resource_user_id