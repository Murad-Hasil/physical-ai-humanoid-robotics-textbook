"""
User model for authentication.

Extends Better-Auth user model with additional fields.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from db.session import Base
from models.base import GUID, TimestampMixin


class User(Base, TimestampMixin):
    """
    User model for authentication.
    
    Attributes:
        id: Unique user identifier
        email: User's email address (unique)
        password_hash: Bcrypt hashed password
        github_id: GitHub OAuth provider ID
        email_verified: Whether email is verified
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login_at: Most recent login timestamp
    """
    
    __tablename__ = "users"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    github_id = Column(String(100), unique=True, nullable=True, index=True)
    email_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False, nullable=False, index=True)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    profile = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    chat_sessions = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    ingestion_logs = relationship(
        "IngestionLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
