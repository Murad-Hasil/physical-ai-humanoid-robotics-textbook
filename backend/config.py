"""
Application configuration.

Loads environment variables and provides settings for the application.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent


class Settings:
    """Application settings from environment variables."""
    
    # API Settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database Settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./physical_ai.db")
    
    # Authentication Settings
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "dev-secret-change-in-production")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-jwt-secret-change-in-production")
    jwt_expiry_hours: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))
    
    # GitHub OAuth Settings
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    
    # CORS Settings
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
    
    # PDF Configuration
    pdf_hardware_reality_page: int = int(os.getenv("PDF_HARDWARE_REALITY_PAGE", "5"))
    pdf_inference_sim_to_real_page: int = int(os.getenv("PDF_INFERENCE_SIM_TO_REAL_PAGE", "8"))
    
    # Grok API Settings (from existing config)
    grok_api_key: str = os.getenv("GROK_API_KEY", "")
    grok_model: str = os.getenv("GROK_MODEL", "grok-beta")
    grok_api_timeout: int = int(os.getenv("GROK_API_TIMEOUT", "30"))
    grok_max_retries: int = int(os.getenv("GROK_MAX_RETRIES", "3"))
    
    # Qdrant Settings (from existing config)
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "physical-ai-docusaurus-textbook")
    
    # Embedding Model Settings (from existing config)
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings.
    
    Returns:
        Settings: Application settings
    """
    return settings
