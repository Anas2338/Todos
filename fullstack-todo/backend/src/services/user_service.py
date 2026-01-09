from sqlmodel import Session, select
from typing import Optional
from uuid import UUID
from models.user import User, UserCreate, UserUpdate
from utils.security import get_password_hash, verify_password
from utils.validators import UserValidation
from utils.observability import get_logger
from fastapi import HTTPException, status


class UserService:
    """Service class for user-related operations."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def create_user(self, session: Session, user_create: UserCreate) -> User:
        """Create a new user with password hashing."""
        # Validate email format
        if not UserValidation.validate_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Validate password strength
        is_valid, error_msg = UserValidation.validate_password_strength(user_create.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Create password hash
        password_hash = get_password_hash(user_create.password)

        # Create new user
        db_user = User(
            email=user_create.email,
            password_hash=password_hash
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        self.logger.info(f"Created new user with ID: {db_user.id}")
        return db_user

    def authenticate_user(self, session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    def get_user_by_id(self, session: Session, user_id: UUID) -> Optional[User]:
        """Get a user by their ID."""
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()

        return user

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        """Get a user by their email."""
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        return user

    def update_user(self, session: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        user = self.get_user_by_id(session, user_id)

        if not user:
            return None

        # Update email if provided
        if user_update.email is not None:
            # Validate email format
            if not UserValidation.validate_email(user_update.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email format"
                )

            # Check if new email is already taken
            existing_user = session.exec(
                select(User).where(User.email == user_update.email)
            ).first()

            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )

            user.email = user_update.email

        # Update password if provided
        if user_update.password is not None:
            # Validate password strength
            is_valid, error_msg = UserValidation.validate_password_strength(user_update.password)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )

            user.password_hash = get_password_hash(user_update.password)

        session.add(user)
        session.commit()
        session.refresh(user)

        self.logger.info(f"Updated user with ID: {user.id}")
        return user

    def delete_user(self, session: Session, user_id: UUID) -> bool:
        """Delete a user by their ID."""
        user = self.get_user_by_id(session, user_id)

        if not user:
            return False

        session.delete(user)
        session.commit()

        self.logger.info(f"Deleted user with ID: {user.id}")
        return True