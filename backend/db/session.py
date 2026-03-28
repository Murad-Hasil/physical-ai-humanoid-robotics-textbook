"""
Database session configuration for SQLAlchemy.

Provides database engine and session factory for the application.
Supports both SQLite (development) and PostgreSQL (production).
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from config import get_settings

# Get settings
settings = get_settings()

# Create database engine with connection pooling for PostgreSQL
if "postgresql" in settings.database_url:
    engine = create_engine(
        settings.database_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Enable connection health checks
        echo=settings.log_level.lower() == "debug",
    )
else:
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        echo=settings.log_level.lower() == "debug",
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
