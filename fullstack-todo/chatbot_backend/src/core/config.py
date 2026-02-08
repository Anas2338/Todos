"""Application configuration module."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Better Auth
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "http://localhost:8000")

    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-1.0-pro-latest")  # Default model


    # MCP Server
    MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8001"))

    # Rate limiting
    RATE_LIMIT_REQUESTS_PER_HOUR: int = int(os.getenv("RATE_LIMIT_REQUESTS_PER_HOUR", "100"))

    # Application
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Validation
    @classmethod
    def validate(cls) -> list[str]:
        """Validate configuration and return list of missing required values."""
        errors = []

        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL is required")

        if not cls.BETTER_AUTH_SECRET:
            errors.append("BETTER_AUTH_SECRET is required")

        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required")

        return errors

# Global config instance
config = Config()

# Validate configuration on import
validation_errors = config.validate()
if validation_errors:
    raise ValueError(f"Configuration validation failed: {', '.join(validation_errors)}")