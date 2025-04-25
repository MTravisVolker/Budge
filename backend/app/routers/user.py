from fastapi import APIRouter
from app.routers.base import BaseRouter
from app.models.user import User
from app.schemas.base import (
    UserCreate,
    UserUpdate,
    UserResponse
)

router = BaseRouter(
    model=User,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    response_schema=UserResponse,
    prefix="/users",
    tags=["users"]
).router
