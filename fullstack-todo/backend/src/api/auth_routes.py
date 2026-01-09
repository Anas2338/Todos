from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from datetime import timedelta, datetime
from models.auth import UserSignupRequest, UserSignupResponse, UserSigninRequest, UserSigninResponse
from models.user import User, UserCreate
from models.password_reset import ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, ResetPasswordResponse, PasswordResetToken
from services.user_service import UserService
from utils.connection_pool import get_session
from utils.security import create_access_token, get_password_hash
from utils.observability import get_logger, create_http_exception
from config.settings import settings
import uuid
import secrets

auth_router = APIRouter()
logger = get_logger(__name__)
user_service = UserService()


@auth_router.post("/auth/signup", response_model=UserSignupResponse, status_code=status.HTTP_201_CREATED)
def signup(user_signup: UserSignupRequest, session: Session = Depends(get_session)):
    """Create a new user account."""
    try:
        # Create user object from signup request
        user_create = UserCreate(
            email=user_signup.email,
            password=user_signup.password
        )

        # Create user via service
        user = user_service.create_user(session, user_create)

        # Return response
        return UserSignupResponse(
            id=str(user.id),
            email=user.email,
            created_at=user.created_at.isoformat()
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during signup"
        )


@auth_router.post("/auth/signin", response_model=UserSigninResponse)
def signin(user_signin: UserSigninRequest, session: Session = Depends(get_session)):
    """Authenticate user and return JWT token."""
    try:
        # Authenticate user
        user = user_service.authenticate_user(
            session,
            user_signin.email,
            user_signin.password
        )

        if not user:
            raise create_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code="INVALID_CREDENTIALS",
                message="Invalid email or password"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        # Return response
        return UserSigninResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=str(user.id)
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during signin: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during signin"
        )


@auth_router.post("/auth/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    forgot_password_request: ForgotPasswordRequest,
    session: Session = Depends(get_session)
):
    """Generate a password reset token and send it to the user's email."""
    try:
        # Find user by email
        user = user_service.get_user_by_email(session, forgot_password_request.email)

        if not user:
            # Don't reveal if the email exists to prevent enumeration attacks
            logger.info(f"Password reset requested for non-existent email: {forgot_password_request.email}")
            return ForgotPasswordResponse(message="If an account with that email exists, a password reset link has been sent.")

        # Generate a secure random token
        reset_token = secrets.token_urlsafe(32)

        # Set expiration time (e.g., 1 hour)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        # Create password reset token record
        password_reset_token = PasswordResetToken(
            user_id=user.id,
            token=reset_token,
            expires_at=expires_at
        )

        # Save the reset token to the database
        session.add(password_reset_token)
        session.commit()

        # In a real implementation, you would send an email here
        # For now, we'll just log the reset token (in production, you'd send it via email)
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        logger.info(f"Password reset link generated for user {user.email}: {reset_link}")

        # TODO: Send email with reset link
        # email_service.send_password_reset_email(user.email, reset_link)

        return ForgotPasswordResponse(message="If an account with that email exists, a password reset link has been sent.")

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during forgot password: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during password reset request"
        )


@auth_router.post("/auth/reset-password", response_model=ResetPasswordResponse)
def reset_password(
    reset_password_request: ResetPasswordRequest,
    session: Session = Depends(get_session)
):
    """Reset user's password using the provided token."""
    try:
        # Find the password reset token
        reset_token_record = session.query(PasswordResetToken).filter(
            PasswordResetToken.token == reset_password_request.token
        ).first()

        if not reset_token_record:
            raise create_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="INVALID_TOKEN",
                message="Invalid or expired password reset token"
            )

        # Check if the token is expired
        if reset_token_record.expires_at < datetime.utcnow():
            # Mark the token as used so it can't be used again
            reset_token_record.used = True
            session.add(reset_token_record)
            session.commit()

            raise create_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="EXPIRED_TOKEN",
                message="Password reset token has expired"
            )

        # Check if the token has already been used
        if reset_token_record.used:
            raise create_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="TOKEN_USED",
                message="Password reset token has already been used"
            )

        # Validate the new password (basic validation)
        if len(reset_password_request.new_password) < 8:
            raise create_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="WEAK_PASSWORD",
                message="Password must be at least 8 characters long"
            )

        # Get the user associated with this reset token
        user = session.get(User, reset_token_record.user_id)
        if not user:
            raise create_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="USER_NOT_FOUND",
                message="User associated with this reset token was not found"
            )

        # Hash the new password
        hashed_password = get_password_hash(reset_password_request.new_password)

        # Update the user's password
        user.hashed_password = hashed_password
        session.add(user)

        # Mark the reset token as used
        reset_token_record.used = True
        session.add(reset_token_record)

        # Commit the changes
        session.commit()

        logger.info(f"Password successfully reset for user {user.email}")

        return ResetPasswordResponse(message="Password has been reset successfully")

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        raise create_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred during password reset"
        )