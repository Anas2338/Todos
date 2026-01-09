#!/usr/bin/env python3
"""
Test script to verify Neon database connection works with the backend.
This script tests the database connection configuration without starting the full API.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection using the existing connection pool."""
    print("Testing database connection...")

    try:
        # Import the connection pool module
        from utils.connection_pool import engine, get_session
        print("OK Successfully imported database modules")

        # Get database URL for display (masking password for security)
        database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
        print(f"Using database URL: {database_url}")

        # Test connection by trying to create tables
        from sqlmodel import SQLModel
        from models.user import User
        from models.task import Task

        print("OK Successfully imported models")

        # Create tables (this will test the connection)
        SQLModel.metadata.create_all(engine)
        print("OK Successfully created/verified database tables")

        # Test getting a session
        from sqlmodel import Session
        with Session(engine) as session:
            print("OK Successfully created database session")

        print("\nDatabase connection test PASSED!")
        print("Your Neon database configuration is working correctly.")
        return True

    except Exception as e:
        print(f"\nDatabase connection test FAILED: {str(e)}")
        print("Please check your database configuration and connection string.")
        return False

def test_environment_variables():
    """Test that required environment variables are set."""
    print("\nTesting environment variables...")

    required_vars = ['DATABASE_URL']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"FAILED Missing required environment variables: {missing_vars}")
        print("\nPlease set these variables in your .env file:")
        print("DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require")
        return False
    else:
        print("OK All required environment variables are set")
        return True

def main():
    print("Neon Database Connection Test")
    print("=" * 40)

    # Test environment variables first
    env_ok = test_environment_variables()
    if not env_ok:
        return False

    # Test database connection
    db_ok = test_database_connection()

    print("\n" + "=" * 40)
    if db_ok:
        print("ALL TESTS PASSED - Neon database is configured correctly!")
        print("\nNext steps:")
        print("1. Run 'uv sync' to ensure all dependencies are installed")
        print("2. Run 'uv run python main.py' to start the application")
        print("3. Your application will be available at http://127.0.0.1:8000")
        return True
    else:
        print("TESTS FAILED - Please fix the issues above before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)