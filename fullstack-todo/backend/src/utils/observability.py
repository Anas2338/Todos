from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import HTTPException
import logging
from pydantic import BaseModel
import time
from functools import wraps


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error_code: str
    message: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None


def create_error_response(error_code: str, message: str, details: Optional[Dict[str, Any]] = None) -> ErrorResponse:
    """Create a standard error response with timestamp."""
    return ErrorResponse(
        error_code=error_code,
        message=message,
        timestamp=datetime.utcnow().isoformat(),
        details=details
    )


def create_http_exception(status_code: int, error_code: str, message: str, details: Optional[Dict[str, Any]] = None):
    """Create an HTTPException with standard error response format."""
    error_response = create_error_response(error_code, message, details)
    return HTTPException(
        status_code=status_code,
        detail=error_response.model_dump()
    )


# Set up logging configuration
def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )


def get_logger(name: str):
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)


def log_api_call(func):
    """Decorator to log API calls with timing information."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger = get_logger(func.__name__)

        # Log the incoming request
        logger.info(f"Starting {func.__name__}")

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            # Log successful completion
            logger.info(f"Completed {func.__name__} in {execution_time:.4f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time

            # Log error
            logger.error(f"Error in {func.__name__} after {execution_time:.4f}s: {str(e)}")
            raise

    return wrapper


# Initialize logging
setup_logging()
logger = get_logger(__name__)