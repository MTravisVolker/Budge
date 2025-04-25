from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.bank_account_instance import BankAccountInstance
from app.schemas.base import (
    BankAccountInstanceCreate,
    BankAccountInstanceUpdate,
    BankAccountInstanceResponse
)

router = BaseRouter(
    model=BankAccountInstance,
    create_schema=BankAccountInstanceCreate,
    update_schema=BankAccountInstanceUpdate,
    response_schema=BankAccountInstanceResponse,
    prefix="/bank-account-instances",
    tags=["bank-account-instances"]
).router
