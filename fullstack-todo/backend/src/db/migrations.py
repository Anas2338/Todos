"""
Database migration setup using Alembic
This module handles database schema migrations
"""
import os
from sqlmodel import SQLModel
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from alembic.operations import Operations
from dotenv import load_dotenv
from ..models.user import User
from ..models.task import Task

# Load environment variables
load_dotenv()

# Import all models to include them in the migration
from ..models.user import User  # noqa: F401
from ..models.task import Task  # noqa: F401
from ..models.token import Token  # noqa: F401

# Define the database models for migration
__all_models__ = [User, Task]


def run_migrations_online():
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine
    from alembic.migration import MigrationContext

    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    # Create engine
    connectable = create_engine(database_url)

    with connectable.connect() as connection:
        ctx = MigrationContext.configure(connection)
        with ctx.begin_transaction():
            # Run migrations
            ctx.run_migrations()


def generate_migration(migration_message: str, autogenerate: bool = True):
    """Generate a new migration file."""
    # Create alembic config
    alembic_cfg = Config("alembic.ini")

    # Generate the migration
    command.revision(alembic_cfg, message=migration_message, autogenerate=autogenerate)


def upgrade_database(revision: str = "head"):
    """Upgrade the database to the specified revision."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, revision)


def downgrade_database(revision: str):
    """Downgrade the database to the specified revision."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, revision)


def create_initial_tables(engine):
    """Create all tables based on models (alternative to migrations for initial setup)."""
    SQLModel.metadata.create_all(engine)