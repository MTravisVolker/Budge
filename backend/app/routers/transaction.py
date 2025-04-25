from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.transaction import Transaction
from app.schemas.base import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse
)

router = BaseRouter(
    model=Transaction,
    create_schema=TransactionCreate,
    update_schema=TransactionUpdate,
    response_schema=TransactionResponse,
    prefix="/transactions",
    tags=["transactions"]
).router
