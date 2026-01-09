"""
Database connection pooling utilities
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,  # Number of connections to maintain in the pool
    max_overflow=30,  # Number of connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False  # Set to True to see SQL queries for debugging
)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session with connection pooling."""
    with Session(engine) as session:
        yield session


def get_engine():
    """Get the database engine with connection pooling."""
    return engine


def get_connection():
    """Get a direct database connection from the pool."""
    return engine.connect()


def dispose_engine():
    """Dispose of the engine and close all connections."""
    engine.dispose()