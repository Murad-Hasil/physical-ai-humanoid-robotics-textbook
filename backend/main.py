"""
FastAPI application for Physical AI Textbook with Authentication.

Main application entry point with all routes registered.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings, get_settings
from models.base import Base
from db.session import engine
from api.auth import router as auth_router
from api.hardware import router as hardware_router
from api.chat import router as chat_router
from api.admin import router as admin_router
from api.user_profiles import router as user_profiles_router
from api.v1.endpoints.personalization import router as personalization_router
from api.v1.endpoints.translations import router as translations_router
from api.v1.endpoints.curriculum import router as curriculum_router
from utils.logger import get_logger, log_security_event

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Physical AI Textbook API with Authentication")
    logger.info(f"Database URL: {settings.database_url}")
    logger.info(f"CORS Origins: {settings.cors_origins}")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Physical AI Textbook API")


# Create FastAPI application
app = FastAPI(
    title="Physical AI Textbook API",
    description="RAG-powered chatbot API with authentication and hardware-aware personalization",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(hardware_router)
app.include_router(chat_router)
app.include_router(admin_router)
app.include_router(user_profiles_router)
app.include_router(personalization_router)
app.include_router(translations_router)
app.include_router(curriculum_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.2.0",
        "timestamp": datetime.utcnow(),
        "services": {
            "database": "connected",
        },
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "service": "Physical AI Textbook API",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/health",
        "auth": "/api/auth",
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions."""
    exc_type = type(exc).__name__
    logger.exception(f"Unhandled exception [{exc_type}]: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred.",
            "error_type": exc_type,
        },
    )


# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
