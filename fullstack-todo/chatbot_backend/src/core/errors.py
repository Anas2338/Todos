"""Custom error handling for the AI Chatbot Backend."""

from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel
import logging


logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base application error class."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self):
        """Convert error to dictionary for JSON response."""
        return {
            "error": {
                "code": self.error_code or "APPLICATION_ERROR",
                "message": self.message,
                "details": self.details
            }
        }


class ValidationError(AppError):
    """Error raised when validation fails."""

    def __init__(self, message: str, field: Optional[str] = None, value: Optional[str] = None):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value

        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=details
        )


class AuthenticationError(AppError):
    """Error raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_FAILED"
        )


class AuthorizationError(AppError):
    """Error raised when authorization fails."""

    def __init__(self, message: str = "Authorization failed"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_FAILED"
        )


class ResourceNotFoundError(AppError):
    """Error raised when a requested resource is not found."""

    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} with ID {resource_id} not found",
            error_code="RESOURCE_NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": resource_id}
        )


class RateLimitExceededError(AppError):
    """Error raised when rate limit is exceeded."""

    def __init__(self, limit: int, window: str, reset_time: int):
        super().__init__(
            message=f"Rate limit exceeded: {limit} requests per {window}",
            error_code="RATE_LIMIT_EXCEEDED",
            details={
                "limit": limit,
                "window": window,
                "reset_time_seconds": reset_time
            }
        )


class DatabaseError(AppError):
    """Error raised when a database operation fails."""

    def __init__(self, message: str, operation: Optional[str] = None):
        details = {}
        if operation:
            details["operation"] = operation

        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details=details
        )


class ExternalServiceError(AppError):
    """Error raised when an external service call fails."""

    def __init__(self, service_name: str, message: str, status_code: Optional[int] = None):
        details = {"service_name": service_name}
        if status_code:
            details["status_code"] = status_code

        super().__init__(
            message=message,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details
        )


class LLMError(ExternalServiceError):
    """Error raised when LLM service call fails."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(
            service_name="LLM Service",
            message=message,
            status_code=status_code
        )


class MCPToolError(AppError):
    """Error raised when an MCP tool call fails."""

    def __init__(self, tool_name: str, message: str):
        super().__init__(
            message=message,
            error_code="MCP_TOOL_ERROR",
            details={"tool_name": tool_name}
        )


# FastAPI exception handlers
def handle_validation_error(exc: ValidationError):
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc.message}, details: {exc.details}")
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=exc.to_dict()
    )


def handle_authentication_error(exc: AuthenticationError):
    """Handle authentication errors."""
    logger.warning(f"Authentication error: {exc.message}")
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exc.to_dict()
    )


def handle_authorization_error(exc: AuthorizationError):
    """Handle authorization errors."""
    logger.warning(f"Authorization error: {exc.message}")
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=exc.to_dict()
    )


def handle_resource_not_found_error(exc: ResourceNotFoundError):
    """Handle resource not found errors."""
    logger.info(f"Resource not found: {exc.message}")
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=exc.to_dict()
    )


def handle_rate_limit_error(exc: RateLimitExceededError):
    """Handle rate limit exceeded errors."""
    logger.warning(f"Rate limit exceeded: {exc.message}")
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=exc.to_dict(),
        headers={"Retry-After": str(exc.details.get("reset_time_seconds", 3600))}
    )


def handle_database_error(exc: DatabaseError):
    """Handle database errors."""
    logger.error(f"Database error: {exc.message}, details: {exc.details}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=exc.to_dict()
    )


def handle_external_service_error(exc: ExternalServiceError):
    """Handle external service errors."""
    logger.error(f"External service error: {exc.message}, service: {exc.details.get('service_name')}")
    # For external service errors, we might want to return a 502 or 503 depending on the situation
    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=exc.to_dict()
    )


def handle_llm_error(exc: LLMError):
    """Handle LLM service errors."""
    logger.error(f"LLM service error: {exc.message}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=exc.to_dict()
    )


def handle_mcp_tool_error(exc: MCPToolError):
    """Handle MCP tool errors."""
    logger.error(f"MCP tool error: {exc.message}, tool: {exc.details.get('tool_name')}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=exc.to_dict()
    )


def handle_generic_error(exc: Exception):
    """Handle generic errors."""
    logger.error(f"Generic error: {str(exc)}", exc_info=True)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred"
            }
        }
    )


# Error response model for documentation
class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: dict