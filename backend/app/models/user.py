from typing import Optional
from sqlalchemy import String, Boolean, Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4
from .base import Base
from .api_token import ApiToken
from .oauth_account import OAuthAccount
from .audit_log import AuditLog
from .bank_account import BankAccount
from .bank_account_instance import BankAccountInstance
from .bills import Bill
from .due_bills import DueBill
from .category import Category
from .recurrence import Recurrence
from .bill_status import BillStatus
from .budget import Budget
from .account import Account
from .transaction import Transaction

class User(Base):
    """User model"""
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
    mfa_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    mfa_secret: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # OAuth fields
    oauth_provider: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    oauth_account_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # Profile fields
    first_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships
    api_tokens: Mapped[list["ApiToken"]] = relationship(back_populates="user")
    oauth_accounts: Mapped[list["OAuthAccount"]] = relationship(back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")
    bank_accounts: Mapped[list["BankAccount"]] = relationship(back_populates="user")
    bank_account_instances: Mapped[list["BankAccountInstance"]] = relationship(back_populates="user")
    bills: Mapped[list["Bill"]] = relationship(back_populates="user")
    due_bills: Mapped[list["DueBill"]] = relationship(back_populates="user")
    categories: Mapped[list["Category"]] = relationship(back_populates="user")
    recurrences: Mapped[list["Recurrence"]] = relationship(back_populates="user")
    bill_statuses: Mapped[list["BillStatus"]] = relationship(back_populates="user")
    budgets: Mapped[list["Budget"]] = relationship(back_populates="user")
    accounts: Mapped[list["Account"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
