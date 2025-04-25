from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.account import Account
from app.schemas.base import (
    AccountCreate,
    AccountUpdate,
    AccountResponse
)

router = BaseRouter(
    model=Account,
    create_schema=AccountCreate,
    update_schema=AccountUpdate,
    response_schema=AccountResponse,
    prefix="/accounts",
    tags=["accounts"]
).router
