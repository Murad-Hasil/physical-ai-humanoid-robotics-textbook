"""
Authorization dependencies for admin-only routes.

Provides dependency injection for admin user verification.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from models.user import User
from auth.jwt_handler import get_current_user
from utils.logger import log_security_event


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Verify user has admin privileges.
    
    This dependency checks if the authenticated user has admin rights.
    Non-admin users receive a 403 Forbidden response.
    
    Args:
        current_user: Authenticated user from JWT token
        db: Database session
        
    Returns:
        User: Admin user
        
    Raises:
        HTTPException: 403 Forbidden if user is not admin
    """
    if not current_user.is_admin:
        log_security_event(
            "UNAUTHORIZED_ADMIN_ACCESS",
            user_id=str(current_user.id),
            email=current_user.email,
            details={"attempted_access": "admin_endpoint"}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "forbidden",
                "message": "Admin access required"
            }
        )
    return current_user
