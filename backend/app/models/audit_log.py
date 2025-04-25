from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .user import User  # Import User for type hints

class AuditLog(Base):
    """Audit Log model"""
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    table_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )
    row_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )
    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    action: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    value_before_change: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    value_after_change: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="audit_logs")

    __table_args__ = (
        CheckConstraint("action IN ('add', 'update', 'delete')", name="check_action"),
    )
