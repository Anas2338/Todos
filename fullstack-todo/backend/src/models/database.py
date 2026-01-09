from sqlmodel import Session
from typing import Generator
from utils.connection_pool import get_session as get_pooled_session, get_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database engine with connection pooling
engine = get_engine()

def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session with connection pooling."""
    with get_pooled_session() as session:
        yield session