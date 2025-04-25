from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.bill_status import BillStatus
from app.schemas.base import (
    BillStatusCreate,
    BillStatusUpdate,
    BillStatusResponse
)

router = BaseRouter(
    model=BillStatus,
    create_schema=BillStatusCreate,
    update_schema=BillStatusUpdate,
    response_schema=BillStatusResponse,
    prefix="/bill-statuses",
    tags=["bill-statuses"]
).router
