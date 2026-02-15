"""
Configuration and environment variables for Pipeline.OS Backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "3001"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./pipeline.db"  # SQLite for development
    )

    # Training Configuration
    MAX_CONCURRENT_TRAININGS: int = int(os.getenv("MAX_CONCURRENT_TRAININGS", "2"))
    TRAINING_TIMEOUT_HOURS: int = int(os.getenv("TRAINING_TIMEOUT_HOURS", "24"))

    # Paths
    MODELS_DIR: str = os.getenv("MODELS_DIR", "./models")
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    CHECKPOINTS_DIR: str = os.getenv("CHECKPOINTS_DIR", "./checkpoints")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Optional: AI/LLM Configuration (for future integration)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton settings instance
settings = Settings()

