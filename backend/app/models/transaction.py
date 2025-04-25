from sqlalchemy import Column, String, ForeignKey, Numeric, Date, Boolean, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.audit_log import AuditLogMixin

class Transaction(Base, AuditLogMixin):
    __tablename__ = "transactions"

    description = Column(String, nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    transaction_date = Column(Date, nullable=False)
    account_id = Column(ForeignKey("accounts.id"), nullable=False)
    category_id = Column(ForeignKey("categories.id"), nullable=True)
    budget_id = Column(ForeignKey("budgets.id"), nullable=True)
    notes = Column(Text, nullable=True)
    archived = Column(Boolean, default=False, nullable=False)

    # Relationships
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    budget = relationship("Budget", back_populates="transactions")
