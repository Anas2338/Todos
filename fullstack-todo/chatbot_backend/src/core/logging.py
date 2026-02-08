"""Application logging configuration."""

import logging
import sys
from typing import Optional
from .config import config
from .logging_setup import setup_logging as setup_structured_logging

def setup_logging() -> None:
    """Configure application logging."""
    # Use the enhanced structured logging setup
    setup_structured_logging(config.LOG_LEVEL, f"logs/app_{config.APP_ENV}.log")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)


# Initialize logging when module is imported
setup_logging()