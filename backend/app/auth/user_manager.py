from datetime import datetime, timedelta
from typing import Optional, cast, Union, Tuple
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_session
from app.models.user import User
from app.config import get_settings
from sqlalchemy.orm import Session
from app.auth.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
import pyotp
from uuid import UUID

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# JWT settings
SECRET_KEY: Union[str, bytes] = str(settings.JWT_SECRET_KEY) if settings.JWT_SECRET_KEY else "your-secret-key"
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class UserManager:
    """User manager for handling authentication"""
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = {}  # In-memory storage for demo purposes

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreate) -> User:
        # Check if user exists
        existing_user = await self.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=True,
            is_verified=False,
            is_superuser=False
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def get_user(self, user_id: UUID) -> Optional[User]:
        return self.users.get(str(user_id))

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self) -> User:
        # This is a placeholder - in a real app, you'd get this from the auth token
        return list(self.users.values())[0]

    async def get_current_active_user(self, current_user: User = Depends(get_current_user)) -> User:
        """Get current active user"""
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    async def enable_mfa(self, user_id: UUID) -> Tuple[str, str]:
        user = await self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        secret = pyotp.random_base32()
        provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            user.email,
            issuer_name="Budget App"
        )

        user.mfa_enabled = True
        user.mfa_secret = secret
        self.db.commit()
        return secret, provisioning_uri

    async def verify_mfa(self, user_id: UUID, code: str) -> bool:
        user = await self.get_user(user_id)
        if not user or not user.mfa_secret:
            return False

        totp = pyotp.TOTP(user.mfa_secret)
        return totp.verify(code)

    async def disable_mfa(self, user_id: UUID) -> None:
        user = await self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        user.mfa_enabled = False
        user.mfa_secret = None
        self.db.commit()

async def get_user_manager(session: AsyncSession = Depends(get_session)) -> UserManager:
    """Get user manager dependency"""
    return UserManager(session)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
