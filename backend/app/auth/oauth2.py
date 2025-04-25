from typing import Dict, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.facebook import FacebookOAuth2
from .config import get_settings
import httpx

settings = get_settings()

# OAuth2 providers configuration
oauth2_providers: Dict[str, Dict] = {
    "google": {
        "client": GoogleOAuth2(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
        ),
        "scopes": ["email", "profile"],
        "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v3/userinfo",
    },
    "facebook": {
        "client": FacebookOAuth2(
            client_id=settings.FACEBOOK_CLIENT_ID,
            client_secret=settings.FACEBOOK_CLIENT_SECRET,
        ),
        "scopes": ["email", "public_profile"],
        "authorize_url": "https://www.facebook.com/v12.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v12.0/oauth/access_token",
        "userinfo_url": "https://graph.facebook.com/v12.0/me",
    },
}

class OAuth2Handler:
    """OAuth2 handler for managing OAuth2 flows"""
    def __init__(self):
        self.providers = ["google", "facebook"]
        self.client = httpx.AsyncClient()

    async def get_authorization_url(self, provider: str) -> str:
        if provider == "google":
            return (
                "https://accounts.google.com/o/oauth2/v2/auth"
                f"?client_id={settings.GOOGLE_CLIENT_ID}"
                "&response_type=code"
                "&scope=email profile"
                f"&redirect_uri={settings.BACKEND_URL}/auth/callback/google"
            )
        elif provider == "facebook":
            return (
                "https://www.facebook.com/v12.0/dialog/oauth"
                f"?client_id={settings.FACEBOOK_CLIENT_ID}"
                "&response_type=code"
                "&scope=email"
                f"&redirect_uri={settings.BACKEND_URL}/auth/callback/facebook"
            )
        raise HTTPException(status_code=400, detail="Invalid provider")

    async def get_access_token(self, provider: str, code: str) -> Optional[Dict]:
        if provider == "google":
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": f"{settings.BACKEND_URL}/auth/callback/google"
            }
        elif provider == "facebook":
            token_url = "https://graph.facebook.com/v12.0/oauth/access_token"
            data = {
                "client_id": settings.FACEBOOK_CLIENT_ID,
                "client_secret": settings.FACEBOOK_CLIENT_SECRET,
                "code": code,
                "redirect_uri": f"{settings.BACKEND_URL}/auth/callback/facebook"
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid provider")

        response = await self.client.post(token_url, data=data)
        if response.status_code != 200:
            return None
        return response.json()

    async def get_user_info(self, provider: str, token: Dict) -> Optional[Dict]:
        if provider == "google":
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {token['access_token']}"}
        elif provider == "facebook":
            user_info_url = f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={token['access_token']}"
            headers = {}
        else:
            raise HTTPException(status_code=400, detail="Invalid provider")

        response = await self.client.get(user_info_url, headers=headers)
        if response.status_code != 200:
            return None
        return response.json()

class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="",  # Will be set dynamically based on provider
    tokenUrl=""  # Will be set dynamically based on provider
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # TODO: Implement token validation and user retrieval
    return token
