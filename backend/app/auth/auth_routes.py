from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.auth.user_manager import UserManager, get_user_manager
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

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
    user_manager: UserManager = Depends(get_user_manager),
    current_user: User = Depends(lambda m=user_manager: m.get_current_active_user()),
) -> Any:
    """Get current user"""
    return current_user
