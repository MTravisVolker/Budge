from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr

class UserRead(schemas.BaseUser[int]):
    """User read schema"""
    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    oauth_provider: Optional[str] = None

    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    """User create schema"""
    email: EmailStr
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    oauth_provider: Optional[str] = None
    oauth_account_id: Optional[str] = None

class UserUpdate(schemas.BaseUserUpdate):
    """User update schema"""
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
