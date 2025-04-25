from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List
from app.models.due_bills import DueBill
from app.models.bank_account_instance import BankAccountInstance
from app.models.recurrence import Recurrence
from sqlalchemy import select, and_

async def calculate_next_due_bill(
    db: AsyncSession,
    due_bill: DueBill,
    background_tasks: BackgroundTasks
) -> None:
    """Calculate and create the next due bill based on recurrence pattern"""
    if not due_bill.recurrence:
        return

    # Get the recurrence pattern
    recurrence = await db.get(Recurrence, due_bill.recurrence_id)
    if not recurrence:
        return

    # Calculate next due date based on recurrence pattern
    next_due_date = calculate_next_date(due_bill.due_date, recurrence.pattern)

    # Create new due bill
    new_due_bill = DueBill(
        bill_id=due_bill.bill_id,
        due_date=next_due_date,
        amount=due_bill.amount,
        status_id=due_bill.status_id,
        recurrence_id=due_bill.recurrence_id,
        user_id=due_bill.user_id
    )

    db.add(new_due_bill)
    await db.commit()

def calculate_next_date(current_date: datetime, pattern: str) -> datetime:
    """Calculate next date based on recurrence pattern"""
    if pattern == "monthly":
        return current_date + timedelta(days=30)
    elif pattern == "biweekly":
        return current_date + timedelta(days=14)
    elif pattern == "weekly":
        return current_date + timedelta(days=7)
    elif pattern == "annually":
        return current_date + timedelta(days=365)
    else:
        # Handle custom patterns (e.g., "every 3 months")
        try:
            num, unit = pattern.split()
            num = int(num)
            if unit == "months":
                return current_date + timedelta(days=30 * num)
            elif unit == "days":
                return current_date + timedelta(days=num)
            else:
                return current_date + timedelta(days=30)  # Default to monthly
        except:
            return current_date + timedelta(days=30)  # Default to monthly

async def update_bank_account_balances(
    db: AsyncSession,
    background_tasks: BackgroundTasks
) -> None:
    """Update bank account balances based on paid bills"""
    # Get all paid bills within the last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    query = select(DueBill).where(
        and_(
            DueBill.status_id == 2,  # Assuming 2 is the ID for "Paid" status
            DueBill.updated_at >= yesterday
        )
    )
    result = await db.execute(query)
    paid_bills = result.scalars().all()

    # Update bank account balances
    for bill in paid_bills:
        if bill.draft_account_id:
            # Get the latest bank account instance
            query = select(BankAccountInstance).where(
                BankAccountInstance.bank_account_id == bill.draft_account_id
            ).order_by(BankAccountInstance.created_at.desc())
            result = await db.execute(query)
            latest_instance = result.scalars().first()

            if latest_instance:
                # Create new instance with updated balance
                new_instance = BankAccountInstance(
                    bank_account_id=bill.draft_account_id,
                    balance=latest_instance.balance - bill.amount,
                    user_id=bill.user_id
                )
                db.add(new_instance)

    await db.commit()

async def cleanup_old_audit_logs(
    db: AsyncSession,
    background_tasks: BackgroundTasks
) -> None:
    """Clean up audit logs older than 90 days"""
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    query = select(AuditLog).where(AuditLog.created_at < ninety_days_ago)
    result = await db.execute(query)
    old_logs = result.scalars().all()

    for log in old_logs:
        await db.delete(log)

    await db.commit()
