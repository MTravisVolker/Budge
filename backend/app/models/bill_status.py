from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class BillStatus(Base):
    """Bill Status model"""
    __tablename__ = "bill_status"

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
    archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    highlight_color_hex: Mapped[Optional[str]] = mapped_column(
        String(7),
        nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="bill_statuses")
    due_bills: Mapped[list["DueBill"]] = relationship(back_populates="status")
    bank_account_instances: Mapped[list["BankAccountInstance"]] = relationship(back_populates="status")
