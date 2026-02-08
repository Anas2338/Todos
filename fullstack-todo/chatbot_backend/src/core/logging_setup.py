"""Enhanced logging setup for debugging and monitoring."""

import logging
import sys
from datetime import datetime
from typing import Dict, Any
import json
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id

        return json.dumps(log_entry)


def setup_logging(log_level: str = "INFO", log_file: str = None) -> logging.Logger:
    """Set up structured logging for the application."""

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Create JSON formatter
    json_formatter = JSONFormatter()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)

    # Reduce noise from third-party libraries
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance."""
    return logging.getLogger(name)


def log_api_request(
    logger: logging.Logger,
    request_method: str,
    request_path: str,
    user_id: str = None,
    session_id: str = None,
    response_status: int = None,
    duration_ms: float = None,
    **extra_fields
):
    """Log an API request with structured data."""
    extra = {
        'request_method': request_method,
        'request_path': request_path,
        'response_status': response_status,
        'duration_ms': duration_ms,
    }
    extra.update(extra_fields)

    if user_id:
        extra['user_id'] = user_id
    if session_id:
        extra['session_id'] = session_id

    logger.info(
        f"{request_method} {request_path} - {response_status}",
        extra=extra
    )


def log_error(
    logger: logging.Logger,
    error_message: str,
    error_type: str,
    user_id: str = None,
    session_id: str = None,
    **extra_fields
):
    """Log an error with structured data."""
    extra = {
        'error_type': error_type,
        'error_message': error_message,
    }
    extra.update(extra_fields)

    if user_id:
        extra['user_id'] = user_id
    if session_id:
        extra['session_id'] = session_id

    logger.error(error_message, extra=extra)


def log_performance(
    logger: logging.Logger,
    operation: str,
    duration_ms: float,
    user_id: str = None,
    session_id: str = None,
    **extra_fields
):
    """Log a performance metric."""
    extra = {
        'operation': operation,
        'duration_ms': duration_ms,
    }
    extra.update(extra_fields)

    if user_id:
        extra['user_id'] = user_id
    if session_id:
        extra['session_id'] = session_id

    logger.info(
        f"Performance: {operation} took {duration_ms}ms",
        extra=extra
    )