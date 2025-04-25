from typing import Type, TypeVar, Generic, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase

from app.database import get_session
from app.auth.user_manager import get_current_user
from app.models.user import User

T = TypeVar('T', bound=DeclarativeBase)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
ResponseSchema = TypeVar('ResponseSchema', bound=BaseModel)

class BaseRouter(Generic[T, CreateSchema, UpdateSchema, ResponseSchema]):
    def __init__(
        self,
        model: Type[T],
        create_schema: Type[CreateSchema],
        update_schema: Type[UpdateSchema],
        response_schema: Type[ResponseSchema],
        prefix: str,
        tags: List[str]
    ):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema

        self.router.add_api_route(
            "/",
            self.create,
            methods=["POST"],
            response_model=response_schema,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/",
            self.list,
            methods=["GET"],
            response_model=List[response_schema]
        )
        self.router.add_api_route(
            "/{id}",
            self.get,
            methods=["GET"],
            response_model=response_schema
        )
        self.router.add_api_route(
            "/{id}",
            self.update,
            methods=["PUT"],
            response_model=response_schema
        )
        self.router.add_api_route(
            "/{id}",
            self.delete,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def create(
        self,
        data: CreateSchema,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ) -> ResponseSchema:
        db_item = self.model(**data.dict(), user_id=current_user.id)
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return self.response_schema.from_orm(db_item)

    async def list(
        self,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
        skip: int = 0,
        limit: int = 100
    ) -> List[ResponseSchema]:
        query = select(self.model).where(self.model.user_id == current_user.id)
        if hasattr(self.model, 'archived'):
            query = query.where(self.model.archived == False)
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        items = result.scalars().all()
        return [self.response_schema.from_orm(item) for item in items]

    async def get(
        self,
        id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ) -> ResponseSchema:
        query = select(self.model).where(
            self.model.id == id,
            self.model.user_id == current_user.id
        )
        result = await session.execute(query)
        item = result.scalar_one_or_none()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )
        return self.response_schema.from_orm(item)

    async def update(
        self,
        id: int,
        data: UpdateSchema,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ) -> ResponseSchema:
        query = select(self.model).where(
            self.model.id == id,
            self.model.user_id == current_user.id
        )
        result = await session.execute(query)
        item = result.scalar_one_or_none()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )

        for key, value in data.dict(exclude_unset=True).items():
            setattr(item, key, value)

        await session.commit()
        await session.refresh(item)
        return self.response_schema.from_orm(item)

    async def delete(
        self,
        id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ) -> None:
        query = select(self.model).where(
            self.model.id == id,
            self.model.user_id == current_user.id
        )
        result = await session.execute(query)
        item = result.scalar_one_or_none()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )

        if hasattr(self.model, 'archived'):
            # Soft delete
            await session.execute(
                update(self.model)
                .where(self.model.id == id)
                .values(archived=True)
            )
        else:
            # Hard delete
            await session.delete(item)

        await session.commit()
