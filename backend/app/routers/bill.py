from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.bill import Bill
from app.schemas.base import (
    BillCreate,
    BillUpdate,
    BillResponse
)

router = BaseRouter(
    model=Bill,
    create_schema=BillCreate,
    update_schema=BillUpdate,
    response_schema=BillResponse,
    prefix="/bills",
    tags=["bills"]
).router
