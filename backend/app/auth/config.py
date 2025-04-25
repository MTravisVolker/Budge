from pydantic_settings import BaseSettings
from functools import lru_cache

class AuthSettings(BaseSettings):
    """Authentication settings"""
    # Database Settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/budg"

    # Google OAuth2 Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "https://localhost:3000/auth/google/callback"

    # Facebook OAuth2 Settings
    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str
    FACEBOOK_REDIRECT_URI: str = "https://localhost:3000/auth/facebook/callback"

    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key"  # Change this in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> AuthSettings:
    """Get cached settings"""
    return AuthSettings()
