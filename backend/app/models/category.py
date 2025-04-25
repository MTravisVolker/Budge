from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .user import User
from .bills import Bill
from .budget import Budget
from .transaction import Transaction

class Category(Base):
    """Category model"""
    __tablename__ = "category"

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

    # Relationships
    user: Mapped["User"] = relationship(back_populates="categories")
    bills: Mapped[list["Bill"]] = relationship(back_populates="category")
    budgets: Mapped[list["Budget"]] = relationship(back_populates="category")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")
