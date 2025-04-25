from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Boolean, ForeignKey, Integer, Numeric, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .user import User
from .recurrence import Recurrence
from .bill_status import BillStatus
from .bank_account import BankAccount

class DueBill(Base):
    """Due Bill model"""
    __tablename__ = "due_bills"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    bill: Mapped[int] = mapped_column(
        ForeignKey("bills.id"),
        nullable=False,
        index=True
    )
    recurrence: Mapped[Optional[int]] = mapped_column(
        ForeignKey("recurrence.id"),
        nullable=True,
        index=True
    )
    recurrence_value: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    priority: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        index=True
    )
    due_date: Mapped[date] = mapped_column(
        nullable=False,
        index=True
    )
    pay_date: Mapped[Optional[date]] = mapped_column(
        nullable=True,
        index=True
    )
    min_amount_due: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    total_amount_due: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    status: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bill_status.id"),
        nullable=True,
        index=True
    )
    archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    confirmation: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    draft_account: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bank_account.id"),
        nullable=True,
        index=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="due_bills")
    bill_obj: Mapped["Bill"] = relationship(back_populates="due_bills")
    recurrence_obj: Mapped["Recurrence"] = relationship(back_populates="due_bills")
    status_obj: Mapped["BillStatus"] = relationship(back_populates="due_bills")
    draft_account_obj: Mapped["BankAccount"] = relationship(back_populates="due_bills")

    __table_args__ = (
        CheckConstraint("recurrence_value > 0", name="check_recurrence_value"),
    )
