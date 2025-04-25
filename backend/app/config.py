from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    # Debug mode
    DEBUG: bool = False

    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:pwd@localhost:5432/budget_app"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "pwd"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "budget_app"

    @property
    def database_url(self) -> str:
        """Get database URL from environment variables or use default"""
        return os.getenv(
            "DATABASE_URL",
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Google OAuth2 Settings
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "https://localhost:3000/auth/google/callback"

    # Facebook OAuth2 Settings
    FACEBOOK_CLIENT_ID: Optional[str] = None
    FACEBOOK_CLIENT_SECRET: Optional[str] = None
    FACEBOOK_REDIRECT_URI: str = "https://localhost:3000/auth/facebook/callback"

    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key"  # Change this in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Frontend settings
    FRONTEND_URL: str = "http://localhost:3000"  # Default frontend URL

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()
