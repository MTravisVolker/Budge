from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.due_bill import DueBill
from app.schemas.base import (
    DueBillCreate,
    DueBillUpdate,
    DueBillResponse
)

router = BaseRouter(
    model=DueBill,
    create_schema=DueBillCreate,
    update_schema=DueBillUpdate,
    response_schema=DueBillResponse,
    prefix="/due-bills",
    tags=["due-bills"]
).router
