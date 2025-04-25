from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.auth.user_manager import UserManager, get_user_manager
from app.models.user import User
from app.auth.schemas import PasswordResetRequest, PasswordResetVerify, PasswordResetComplete, MFAEnableRequest, MFAVerifyRequest
from jose.exceptions import JWTError
import pyotp

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

@router.post("/password-reset/request", status_code=status.HTTP_200_OK)
async def request_password_reset(
    data: PasswordResetRequest,
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Request password reset"""
    user = await user_manager.get_user_by_email(data.email)
    if user:
        # In a real app, you would send an email with the reset token
        reset_token = user_manager.create_access_token(
            data={"sub": user.email, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        # TODO: Send email with reset token
        return {"message": "If an account exists with this email, you will receive a password reset link"}
    return {"message": "If an account exists with this email, you will receive a password reset link"}

@router.post("/password-reset/verify", status_code=status.HTTP_200_OK)
async def verify_password_reset(
    data: PasswordResetVerify,
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Verify password reset token"""
    try:
        payload = user_manager.decode_token(data.token)
        if payload.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
        return {"message": "Token is valid"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

@router.post("/password-reset/complete", status_code=status.HTTP_200_OK)
async def complete_password_reset(
    data: PasswordResetComplete,
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Complete password reset"""
    try:
        payload = user_manager.decode_token(data.token)
        if payload.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
        email = payload.get("sub")
        user = await user_manager.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        user.hashed_password = user_manager.get_password_hash(data.new_password)
        await user_manager.db.commit()
        return {"message": "Password has been reset"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

@router.post("/mfa/enable", status_code=status.HTTP_200_OK)
async def enable_mfa(
    data: MFAEnableRequest,
    current_user: User = Depends(get_current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Enable multifactor authentication"""
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )
    # Generate TOTP secret
    secret = pyotp.random_base32()
    # Generate provisioning URI
    provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        current_user.email,
        issuer_name="Budge"
    )
    # Store secret temporarily (in a real app, you would store this securely)
    current_user.mfa_secret = secret
    await user_manager.db.commit()
    return {
        "secret": secret,
        "provisioning_uri": provisioning_uri
    }

@router.post("/mfa/verify", status_code=status.HTTP_200_OK)
async def verify_mfa(
    data: MFAVerifyRequest,
    current_user: User = Depends(get_current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Verify multifactor authentication setup"""
    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )
    # Verify TOTP code
    totp = pyotp.TOTP(current_user.mfa_secret)
    if not totp.verify(data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid code"
        )
    # Enable MFA
    current_user.mfa_enabled = True
    await user_manager.db.commit()
    return {"message": "MFA has been enabled"}

@router.post("/mfa/disable", status_code=status.HTTP_200_OK)
async def disable_mfa(
    current_user: User = Depends(get_current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """Disable multifactor authentication"""
    if not current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )
    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    await user_manager.db.commit()
    return {"message": "MFA has been disabled"}
