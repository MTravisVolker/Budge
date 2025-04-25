from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.budget import Budget
from app.schemas.base import (
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse
)

router = BaseRouter(
    model=Budget,
    create_schema=BudgetCreate,
    update_schema=BudgetUpdate,
    response_schema=BudgetResponse,
    prefix="/budgets",
    tags=["budgets"]
).router
