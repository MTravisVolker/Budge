from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.bank_account import BankAccount
from app.schemas.base import (
    BankAccountCreate,
    BankAccountUpdate,
    BankAccountResponse
)

router = BaseRouter(
    model=BankAccount,
    create_schema=BankAccountCreate,
    update_schema=BankAccountUpdate,
    response_schema=BankAccountResponse,
    prefix="/bank-accounts",
    tags=["bank-accounts"]
).router
