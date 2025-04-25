from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, ForeignKey, Integer, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .user import User  # Import User for type hints
from .bank_account import BankAccount  # Import BankAccount for type hints
from .category import Category  # Import Category for type hints
from .recurrence import Recurrence  # Import Recurrence for type hints

class Bill(Base):
    """Bill model"""
    __tablename__ = "bills"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )
    default_amount_due: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    url: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    default_draft_account: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bank_account.id"),
        nullable=True,
        index=True
    )
    category: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("category.id"),
        nullable=True,
        index=True
    )
    recurrence: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("recurrence.id"),
        nullable=True,
        index=True
    )
    recurrence_value: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="bills")
    default_draft_account_obj: Mapped[Optional["BankAccount"]] = relationship(back_populates="bills")
    category_obj: Mapped[Optional["Category"]] = relationship(back_populates="bills")
    recurrence_obj: Mapped[Optional["Recurrence"]] = relationship(back_populates="bills")
    due_bills: Mapped[list["DueBill"]] = relationship(back_populates="bill")

    __table_args__ = (
        CheckConstraint("url ~ '^https?://'", name='check_url_format'),
        CheckConstraint('recurrence_value > 0', name='check_recurrence_value'),
    )
