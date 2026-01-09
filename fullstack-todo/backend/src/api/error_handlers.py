from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.observability import ErrorResponse, create_error_response
from utils.observability import get_logger
from typing import Dict, Any
import traceback


def setup_error_handlers(app: FastAPI):
    """Set up comprehensive error handlers for the application."""

    logger = get_logger(__name__)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions with standard error response format."""
        logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")

        # If detail is already in standard error format, use it directly
        if isinstance(exc.detail, dict) and "error_code" in exc.detail:
            error_response = ErrorResponse(
                error_code=exc.detail.get("error_code", "UNKNOWN_ERROR"),
                message=exc.detail.get("message", "An unknown error occurred"),
                timestamp=exc.detail.get("timestamp"),
                details=exc.detail.get("details")
            )
        else:
            # Create standard error response
            error_response = create_error_response(
                error_code="HTTP_ERROR",
                message=str(exc.detail) if exc.detail else "HTTP error occurred",
                details={"status_code": exc.status_code}
            )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors with standard error response format."""
        logger.error(f"Validation Error: {exc}")

        error_details = []
        for error in exc.errors():
            error_details.append({
                "field": ".".join(str(loc) for loc in error['loc']),
                "message": error['msg'],
                "type": error['type']
            })

        error_response = create_error_response(
            error_code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": error_details}
        )

        return JSONResponse(
            status_code=422,
            content=error_response.model_dump()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions with standard error response format."""
        logger.error(f"General Exception: {str(exc)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

        error_response = create_error_response(
            error_code="INTERNAL_ERROR",
            message="An internal server error occurred",
            details={
                "error_type": type(exc).__name__,
                "error_message": str(exc)
            }
        )

        return JSONResponse(
            status_code=500,
            content=error_response.model_dump()
        )

    return app