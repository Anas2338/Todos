"""Database connection and session management."""

from sqlmodel import create_engine, Session
from sqlalchemy import event
from contextlib import contextmanager
from typing import Generator
from .config import config
import logging

# Create the database engine with enhanced connection settings for Neon
engine = create_engine(
    config.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
)

# Add connection event listeners for debugging
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set connection parameters for Neon PostgreSQL."""
    import os
    if 'neon.tech' in config.DATABASE_URL:
        # Enable SSL and set appropriate parameters for Neon
        pass  # SQLAlchemy handles Neon SSL automatically

logger = logging.getLogger(__name__)

def get_session() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:
        yield session

@contextmanager
def get_session_context():
    """Get a database session with context management."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        session.close()

def init_db():
    """Initialize the database (create tables if they don't exist)."""
    import logging
    logger = logging.getLogger(__name__)

    try:
        from ..models.base import SQLModel
        # Import all models to register them with SQLModel
        from ..models.chat_session import ChatSession
        from ..models.chat_message import ChatMessage
        from ..models.tool_invocation import ToolInvocation
        from ..models.task import Task

        # Create all tables
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully.")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def close_db():
    """Close the database engine."""
    engine.dispose()