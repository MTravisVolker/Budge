from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.core.background_tasks import (
    update_bank_account_balances,
    cleanup_old_audit_logs
)

def init_scheduler(app: FastAPI) -> None:
    """Initialize background task scheduler"""

    @app.on_event("startup")
    @repeat_every(seconds=60 * 60)  # Run every hour
    async def update_balances() -> None:
        """Update bank account balances"""
        async with get_session() as session:
            await update_bank_account_balances(session, app.background_tasks)

    @app.on_event("startup")
    @repeat_every(seconds=60 * 60 * 24)  # Run daily
    async def cleanup_logs() -> None:
        """Clean up old audit logs"""
        async with get_session() as session:
            await cleanup_old_audit_logs(session, app.background_tasks)
