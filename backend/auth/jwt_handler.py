"""
JWT handler for token validation and user retrieval.

Provides dependency injection for JWT token validation.
"""

import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.session import get_db
from models.user import User
from auth.session_validator import decode_access_token
from utils.logger import log_security_event

logger = logging.getLogger(__name__)

# Security scheme for Bearer token
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.

    This dependency validates the JWT token and retrieves the user from database.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        User: Authenticated user

    Raises:
        HTTPException: 401 Unauthorized if token invalid or missing
        HTTPException: 404 Not Found if user not found
    """
    # Check if credentials provided
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "unauthorized",
                "message": "Authentication required"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token
    token = credentials.credentials

    try:
        # Verify token and get user ID
        payload = decode_access_token(token)
        user_id = payload.get("sub") if payload else None

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "unauthorized",
                    "message": "Invalid token"
                },
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "user_not_found",
                    "message": "User not found"
                }
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        log_security_event(
            "INVALID_TOKEN",
            details={"error": str(e)},
            level="WARNING",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "unauthorized",
                "message": "Invalid or expired token"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
