"""
Logging utility for the application.

Provides configured logger with security event logging support.
"""

import logging
import sys
from pathlib import Path

from config import get_settings

settings = get_settings()

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    
    # Set log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


def log_security_event(
    event_type: str,
    user_id: str | None = None,
    details: dict | None = None,
    level: str = "INFO",
):
    """
    Log a security-relevant event.
    
    Args:
        event_type: Type of security event (e.g., "login_attempt", "auth_failure")
        user_id: User ID if available
        details: Additional event details
        level: Log level (INFO, WARNING, ERROR)
    """
    logger = get_logger("security")
    
    log_entry = {
        "event_type": event_type,
        "user_id": user_id,
        "details": details or {},
    }
    
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"SECURITY_EVENT: {log_entry}")


# Example security event types
SECURITY_EVENTS = {
    "LOGIN_ATTEMPT": "User login attempt",
    "LOGIN_SUCCESS": "Successful login",
    "LOGIN_FAILURE": "Failed login attempt",
    "LOGOUT": "User logout",
    "TOKEN_VALIDATION": "Token validation",
    "TOKEN_EXPIRED": "Token expired",
    "UNAUTHORIZED_ACCESS": "Unauthorized access attempt",
    "RATE_LIMIT_EXCEEDED": "Rate limit exceeded",
    "PASSWORD_CHANGE": "Password change",
    "ACCOUNT_CREATED": "New account created",
}
