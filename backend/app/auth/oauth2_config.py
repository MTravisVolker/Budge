from typing import Dict
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.authentication.strategy import Strategy
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.facebook import FacebookOAuth2
from .config import get_settings

settings = get_settings()

# Bearer transport for JWT
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# JWT Strategy
def get_jwt_strategy() -> Strategy:
    """Return the JWT strategy"""
    return JWTStrategy(
        secret=settings.JWT_SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

# Authentication backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# OAuth2 clients
google_oauth_client = GoogleOAuth2(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
)

facebook_oauth_client = FacebookOAuth2(
    client_id=settings.FACEBOOK_CLIENT_ID,
    client_secret=settings.FACEBOOK_CLIENT_SECRET,
)

# OAuth2 configurations
oauth2_configs: Dict = {
    "google": {
        "client": google_oauth_client,
        "redirect_url": settings.GOOGLE_REDIRECT_URI,
        "name": "Google",
    },
    "facebook": {
        "client": facebook_oauth_client,
        "redirect_url": settings.FACEBOOK_REDIRECT_URI,
        "name": "Facebook",
    },
}
