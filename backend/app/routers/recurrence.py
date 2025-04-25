from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.recurrence import Recurrence
from app.schemas.base import (
    RecurrenceCreate,
    RecurrenceUpdate,
    RecurrenceResponse
)

router = BaseRouter(
    model=Recurrence,
    create_schema=RecurrenceCreate,
    update_schema=RecurrenceUpdate,
    response_schema=RecurrenceResponse,
    prefix="/recurrences",
    tags=["recurrences"]
).router
