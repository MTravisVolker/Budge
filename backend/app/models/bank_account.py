from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, ForeignKey, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .user import User  # Import User for type hints
from .recurrence import Recurrence  # Import Recurrence for type hints

class BankAccount(Base):
    """Bank Account model"""
    __tablename__ = "bank_account"

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
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )
    url: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
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
    archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    font_color_hex: Mapped[str] = mapped_column(
        String(7),
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="bank_accounts")
    recurrence_obj: Mapped[Optional["Recurrence"]] = relationship(back_populates="bank_accounts")
    instances: Mapped[list["BankAccountInstance"]] = relationship(back_populates="bank_account")
    bills: Mapped[list["Bill"]] = relationship(back_populates="default_draft_account")
    due_bills: Mapped[list["DueBill"]] = relationship(back_populates="draft_account")

    __table_args__ = (
        CheckConstraint("font_color_hex ~ '^#[0-9A-Fa-f]{6}$'", name='check_font_color_hex'),
        CheckConstraint("url ~ '^https?://'", name='check_url_format'),
        CheckConstraint('recurrence_value > 0', name='check_recurrence_value'),
    )
