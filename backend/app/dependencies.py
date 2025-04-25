from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency"""
    async for session in get_session():
        yield session

# Example of how to use the dependency in a route:
# @router.get("/items")
# async def get_items(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Item))
#     return result.scalars().all()
