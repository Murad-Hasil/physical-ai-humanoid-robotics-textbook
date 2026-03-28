"""
Authentication service for user registration, login, and session management.

Provides business logic for authentication operations.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from models.student_profile import StudentProfile
from auth.session_validator import get_password_hash, verify_password, create_access_token
from utils.logger import log_security_event

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service for user management."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            User: Created user
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            log_security_event(
                "ACCOUNT_CREATED",
                details={"email": email, "status": "failed_duplicate"},
                level="WARNING",
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "conflict",
                    "message": "An account with this email already exists",
                },
            )
        
        # Create user
        user = User(
            email=email,
            password_hash=get_password_hash(password),
            email_verified=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Create student profile
        profile = StudentProfile(user_id=user.id)
        self.db.add(profile)
        self.db.commit()
        
        log_security_event(
            "ACCOUNT_CREATED",
            user_id=str(user.id),
            details={"email": email, "status": "success"},
        )
        
        logger.info(f"User registered: {email}")
        return user
    
    def login(self, email: str, password: str) -> tuple[User, str]:
        """
        Authenticate user and return user + access token.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            tuple[User, str]: User and access token
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user or not user.password_hash:
            log_security_event(
                "LOGIN_FAILURE",
                details={"email": email, "reason": "user_not_found_or_oauth"},
                level="WARNING",
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "invalid_credentials",
                    "message": "Invalid email or password",
                },
            )
        
        # Verify password
        if not verify_password(password, user.password_hash):
            log_security_event(
                "LOGIN_FAILURE",
                user_id=str(user.id),
                details={"email": email, "reason": "wrong_password"},
                level="WARNING",
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "invalid_credentials",
                    "message": "Invalid email or password",
                },
            )
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        # Update last login
        user.last_login_at = __import__('datetime').datetime.utcnow()
        self.db.commit()
        
        log_security_event(
            "LOGIN_SUCCESS",
            user_id=str(user.id),
            details={"email": email},
        )
        
        logger.info(f"User logged in: {email}")
        return user, access_token
    
    def logout(self, user_id: str) -> None:
        """
        Logout user (invalidate session).
        
        Args:
            user_id: User ID
        """
        log_security_event(
            "LOGOUT",
            user_id=user_id,
            details={},
        )
        logger.info(f"User logged out: {user_id}")
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[User]: User or None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User or None
        """
        return self.db.query(User).filter(User.email == email).first()
