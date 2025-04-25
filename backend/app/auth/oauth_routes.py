from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.auth.oauth2 import OAuth2Handler
from app.auth.user_manager import UserManager
from app.auth.schemas import UserCreate
from app.config import settings
import secrets

router = APIRouter(prefix="/auth")
oauth_handler = OAuth2Handler()
user_manager = UserManager()

@router.get("/login/{provider}")
async def login(provider: str):
    if provider not in oauth_handler.providers:
        raise HTTPException(status_code=400, detail="Invalid provider")

    auth_url = await oauth_handler.get_authorization_url(provider)
    return RedirectResponse(url=auth_url)

@router.get("/callback/{provider}")
async def callback(provider: str, request: Request):
    if provider not in oauth_handler.providers:
        raise HTTPException(status_code=400, detail="Invalid provider")

    # Get the authorization code from the request
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    # Get access token
    token = await oauth_handler.get_access_token(provider, code)
    if not token:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    # Get user info
    user_info = await oauth_handler.get_user_info(provider, token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info")

    # Check if user exists
    user = await user_manager.get_user_by_email(user_info["email"])
    if not user:
        # Create a random password for OAuth users
        random_password = secrets.token_urlsafe(16)
        user_create = UserCreate(
            email=user_info["email"],
            password=random_password,
            full_name=user_info.get("name", ""),
            is_oauth=True
        )
        user = await user_manager.create_user(user_create)

    # Generate JWT token
    access_token = user_manager.create_access_token(data={"sub": user.email})

    # Redirect to frontend with token
    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/auth/callback?token={access_token}"
    )
