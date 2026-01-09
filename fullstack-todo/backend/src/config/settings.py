from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "")
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-here-replace-with-actual-secure-key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Password hashing
    bcrypt_rounds: int = int(os.getenv("BCRYPT_ROUNDS", "12"))

    # Rate limiting
    rate_limit: str = os.getenv("RATE_LIMIT", "100/hour")
    rate_limit_max_requests: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"

settings = Settings()