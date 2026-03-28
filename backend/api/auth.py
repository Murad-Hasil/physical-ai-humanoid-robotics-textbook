"""
Authentication API endpoints.

Provides REST API for user registration, login, logout, and session management.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from db.session import get_db
from auth.auth_service import AuthService
from auth.middleware import get_current_user, require_auth, UserContext
from auth.session_validator import create_access_token
from models.user import User
from utils.logger import log_security_event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# Request/Response Models
class RegisterRequest(BaseModel):
    """Registration request model."""
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    email_verified: bool
    is_admin: bool = False
    created_at: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response model."""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


# Endpoints
@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user with email and password.
    
    **Request:**
    - `email`: Valid email address
    - `password`: Password (minimum 8 characters)
    
    **Response:**
    - User information and access token
    """
    auth_service = AuthService(db)
    user = auth_service.register(request.email, request.password)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return LoginResponse(
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            email_verified=user.email_verified,
            is_admin=user.is_admin,
            created_at=user.created_at.isoformat(),
        ),
        access_token=access_token,
    )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user with email and password.
    
    **Request:**
    - `email`: User email
    - `password`: User password
    
    **Response:**
    - User information and access token
    
    **Errors:**
    - 401: Invalid credentials
    """
    auth_service = AuthService(db)
    user, access_token = auth_service.login(request.email, request.password)
    
    return LoginResponse(
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            email_verified=user.email_verified,
            is_admin=user.is_admin,
            created_at=user.created_at.isoformat(),
        ),
        access_token=access_token,
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Logout current user.
    
    **Requires:** Authentication
    """
    auth_service = AuthService(db)
    auth_service.logout(user.user_id)
    
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current(
    user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Get current authenticated user.

    **Requires:** Authentication

    **Response:**
    - Current user information including is_admin flag
    """
    db_user = db.query(User).filter(User.id == user.user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=str(db_user.id),
        email=db_user.email,
        email_verified=db_user.email_verified,
        is_admin=db_user.is_admin,
        created_at=db_user.created_at.isoformat(),
    )


@router.get("/github")
async def login_with_github():
    """
    Initiate GitHub OAuth login.
    
    Redirects user to GitHub OAuth authorization page.
    """
    # TODO: Implement GitHub OAuth flow
    # For now, return a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="GitHub OAuth not yet implemented",
    )


@router.get("/github/callback")
async def github_callback(
    code: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Handle GitHub OAuth callback.
    
    **Query Parameters:**
    - `code`: OAuth authorization code
    """
    # TODO: Implement GitHub OAuth callback
    # For now, return a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="GitHub OAuth callback not yet implemented",
    )
