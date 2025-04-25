from datetime import datetime, date
from typing import Optional
from sqlalchemy import ForeignKey, Integer, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .user import User  # Import User for type hints
from .bank_account import BankAccount  # Import BankAccount for type hints
from .bill_status import BillStatus  # Import BillStatus for type hints

class BankAccountInstance(Base):
    """Bank Account Instance model"""
    __tablename__ = "bank_account_instance"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    bank_account: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bank_account.id"),
        nullable=False,
        index=True
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
    status: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("bill_status.id"),
        nullable=True,
        index=True
    )
    archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    current_balance: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="bank_account_instances")
    bank_account_obj: Mapped["BankAccount"] = relationship(back_populates="instances")
    status_obj: Mapped[Optional["BillStatus"]] = relationship(back_populates="bank_account_instances")
