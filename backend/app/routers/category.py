from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.category import Category
from app.schemas.base import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

router = BaseRouter(
    model=Category,
    create_schema=CategoryCreate,
    update_schema=CategoryUpdate,
    response_schema=CategoryResponse,
    prefix="/categories",
    tags=["categories"]
).router
