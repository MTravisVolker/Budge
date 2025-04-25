from sqlalchemy import Column, String, ForeignKey, Numeric, Date, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.audit_log import AuditLogMixin

class Budget(Base, AuditLogMixin):
    __tablename__ = "budgets"

    name = Column(String, nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    category_id = Column(ForeignKey("categories.id"), nullable=True)
    archived = Column(Boolean, default=False, nullable=False)

    # Relationships
    category = relationship("Category", back_populates="budgets")
    transactions = relationship("Transaction", back_populates="budget")
