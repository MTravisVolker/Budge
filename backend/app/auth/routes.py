from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi_users import FastAPIUsers
from .oauth2_config import oauth2_configs, auth_backend
from .users import get_user_manager
from .models import User
from .schemas import UserRead, UserCreate, UserUpdate
from datetime import timedelta
from typing import Any
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.auth.user_manager import UserManager

# Create FastAPI Users instance
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Create router
router = APIRouter(prefix="/auth", tags=["auth"])

# Include FastAPI Users routes
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/register",
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/verify",
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset-password",
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)

# OAuth routes
@router.get("/{provider}/login")
async def oauth_login(provider: str, request: Request):
    """Redirect to OAuth provider login"""
    if provider not in oauth2_configs:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not supported")

    config = oauth2_configs[provider]
    client = config["client"]
    redirect_url = config["redirect_url"]

    authorization_url = await client.get_authorization_url(
        redirect_url,
        scope=["email", "profile"] if provider == "google" else ["email"],
    )
    return RedirectResponse(authorization_url)

@router.get("/{provider}/callback")
async def oauth_callback(
    provider: str,
    code: str,
    request: Request,
    user_manager=Depends(get_user_manager),
):
    """Handle OAuth callback"""
    if provider not in oauth2_configs:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not supported")

    config = oauth2_configs[provider]
    client = config["client"]
    redirect_url = config["redirect_url"]

    try:
        access_token = await client.get_access_token(code, redirect_url)
        user_data = await client.get_id_email(access_token["access_token"])

        user = await user_manager.oauth_callback(
            oauth_name=provider,
            access_token=access_token["access_token"],
            account_id=user_data.id,
            account_email=user_data.email,
            expires_at=access_token.get("expires_at"),
            refresh_token=access_token.get("refresh_token"),
            request=request,
            associate_by_email=True,
            is_verified_by_default=True,
        )

        # Create response with auth token
        response = RedirectResponse(url="/dashboard")
        await auth_backend.get_strategy().write_token(response, user)
        return response

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to authenticate with {provider.capitalize()}: {str(e)}",
        )

class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response model"""
    id: int
    email: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Register new user"""
    user = await user_manager.create_user(
        email=user_data.email,
        password=user_data.password,
    )
    return user

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Login user and get access token"""
    user = await user_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=30)
    access_token = user_manager.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_user_manager().get_current_active_user),
) -> Any:
    """Get current user"""
    return current_user
