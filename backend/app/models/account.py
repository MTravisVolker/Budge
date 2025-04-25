from sqlalchemy import Column, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.audit_log import AuditLogMixin

class Account(Base, AuditLogMixin):
    __tablename__ = "accounts"

    name = Column(String, nullable=False)
    balance = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
    account_type = Column(String, nullable=False)  # checking, savings, credit, etc.
    bank_account_id = Column(ForeignKey("bank_accounts.id"), nullable=True)
    archived = Column(Boolean, default=False, nullable=False)

    # Relationships
    bank_account = relationship("BankAccount", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
