from typing import Optional
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()

class User(SQLAlchemyBaseUserTable[int], Base):
    """User model for authentication"""
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(length=1024), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # OAuth-specific fields
    oauth_provider: Mapped[Optional[str]] = mapped_column(
        String(length=20), nullable=True
    )
    oauth_account_id: Mapped[Optional[str]] = mapped_column(
        String(length=320), nullable=True
    )

    # User profile fields
    first_name: Mapped[Optional[str]] = mapped_column(
        String(length=50), nullable=True
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(length=50), nullable=True
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(length=1024), nullable=True
    )
