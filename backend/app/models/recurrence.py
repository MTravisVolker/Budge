from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Recurrence(Base):
    """Recurrence model"""
    __tablename__ = "recurrence"

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
    calculation: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )
    archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="recurrences")
    bank_accounts: Mapped[list["BankAccount"]] = relationship(back_populates="recurrence")
    due_bills: Mapped[list["DueBill"]] = relationship(back_populates="recurrence")
