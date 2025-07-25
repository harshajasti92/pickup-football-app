"""
Configuration settings for the Pickup Football API
"""
import os
from typing import Dict, Any

class Settings:
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "Pickup Football API"
    API_VERSION: str = "1.0.0"
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]
    
    # Database Settings
    DATABASE_CONFIG: Dict[str, Any] = {
        "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "database": os.getenv("POSTGRES_DATABASE", "pickup_football"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "kingdoms"),
        "port": int(os.getenv("POSTGRES_PORT", "5432"))
    }
    
    # Security Settings
    BCRYPT_ROUNDS: int = 12
    
    # Game Settings
    DEFAULT_GAME_DURATION: int = 90
    DEFAULT_MAX_PLAYERS: int = 22
    MIN_GAME_DURATION: int = 30
    MAX_GAME_DURATION: int = 180
    MIN_PLAYERS: int = 4
    MAX_PLAYERS: int = 30
    MIN_SKILL_LEVEL: int = 1
    MAX_SKILL_LEVEL: int = 10

# Create settings instance
settings = Settings()
