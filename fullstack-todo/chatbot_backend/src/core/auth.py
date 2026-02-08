"""Authentication middleware supporting both Better Auth and Main Backend JWT tokens."""

from fastapi import HTTPException, Depends, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import httpx
from .config import config
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from uuid import UUID


class AuthMiddleware:
    """Support for both Better Auth and Main Backend JWT tokens."""

    def __init__(self):
        self.auth_scheme = HTTPBearer()
        self.auth_url = config.BETTER_AUTH_URL
        self.better_auth_secret = config.BETTER_AUTH_SECRET
        # Use the same secret as main backend for JWT compatibility
        self.main_backend_secret = config.BETTER_AUTH_SECRET  # Both use the same secret

    async def verify_better_auth_token(self, token: str) -> Dict[str, Any]:
        """Verify Better Auth token and return user information."""
        try:
            # Decode the Better Auth JWT token using the secret
            payload = jwt.decode(token, self.better_auth_secret, algorithms=["HS256"])

            # Extract user information (Better Auth format)
            user_id = payload.get("userId") or payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: no userId")

            # Convert user_id to UUID if it's a string
            if isinstance(user_id, str):
                try:
                    user_id = UUID(user_id)
                except ValueError:
                    raise HTTPException(status_code=401, detail="Invalid user ID format")

            # Return user info
            return {
                "user_id": user_id,
                "exp": payload.get("exp"),
                "iat": payload.get("iat"),
                "email": payload.get("email", ""),
            }

        except PyJWTError:
            # Not a valid Better Auth token, let's try main backend format
            return None
        except Exception:
            # Some other error, let's try main backend format
            return None

    async def verify_main_backend_token(self, token: str) -> Dict[str, Any]:
        """Verify Main Backend JWT token and return user information."""
        try:
            # Decode the Main Backend JWT token using the same secret
            payload = jwt.decode(token, self.main_backend_secret, algorithms=["HS256"])

            # Extract user information (Main Backend format)
            user_id = payload.get("sub")  # Main backend uses "sub" for user ID
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: no user ID")

            # Convert user_id to UUID if it's a string
            if isinstance(user_id, str):
                try:
                    user_id = UUID(user_id)
                except ValueError:
                    raise HTTPException(status_code=401, detail="Invalid user ID format")

            # Return user info
            return {
                "user_id": user_id,
                "exp": payload.get("exp"),
                "iat": payload.get("iat"),
                "email": payload.get("email", ""),
            }

        except PyJWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")

    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify the authentication token (either Better Auth or Main Backend) and return user information."""
        # First try to verify as Better Auth token
        better_auth_result = await self.verify_better_auth_token(token)

        if better_auth_result is not None:
            # Successfully verified as Better Auth token
            return better_auth_result

        # If Better Auth verification failed, try Main Backend format
        return await self.verify_main_backend_token(token)

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Get the current authenticated user from the token."""
        return await self.verify_token(credentials.credentials)


# Global instance of the auth middleware
auth_middleware = AuthMiddleware()


# Dependency for protected routes
async def get_current_user(request: Request) -> Dict[str, Any]:
    """Dependency to get the current authenticated user."""
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.split(" ")[1]
    return await auth_middleware.verify_token(token)


# Alternative dependency for optional authentication
async def get_optional_user(request: Request) -> Optional[Dict[str, Any]]:
    """Dependency to get the current authenticated user if present."""
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    try:
        token = auth_header.split(" ")[1]
        return await auth_middleware.verify_token(token)
    except HTTPException:
        return None