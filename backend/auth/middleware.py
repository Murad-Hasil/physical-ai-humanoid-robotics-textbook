"""
FastAPI authentication middleware.

Provides dependency injection for authentication and session validation.
"""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.session_validator import validate_session_token
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# HTTP Bearer token security
security = HTTPBearer(auto_error=False)


class UserContext:
    """User context from authentication token."""
    
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email
    
    def __repr__(self):
        return f"UserContext(user_id={self.user_id}, email={self.email})"


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[UserContext]:
    """
    Get current authenticated user from token.
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        UserContext: Current user information
        
    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    
    # Validate token
    payload = validate_session_token(token)
    
    if not payload:
        logger.warning("Invalid or expired token")
        return None
    
    user_id = payload.get("user_id")
    email = payload.get("email")
    
    if not user_id or not email:
        logger.warning("Token missing required fields")
        return None
    
    return UserContext(user_id=user_id, email=email)


async def require_auth(
    user: Optional[UserContext] = Depends(get_current_user),
) -> UserContext:
    """
    Require authentication for endpoint.
    
    Args:
        user: Current user from get_current_user
        
    Returns:
        UserContext: Authenticated user
        
    Raises:
        HTTPException: If not authenticated
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "unauthorized",
                "message": "Authentication required. Please log in.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def log_security_event(event_type: str, user_id: Optional[str], details: dict):
    """
    Log security-relevant events.
    
    Args:
        event_type: Type of security event
        user_id: User ID if available
        details: Additional event details
    """
    log_entry = {
        "event_type": event_type,
        "user_id": user_id,
        "details": details,
    }
    logger.info(f"Security Event: {log_entry}")
