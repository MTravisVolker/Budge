from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class UserBase(BaseSchema):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    mfa_enabled: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

class BillStatusBase(BaseSchema):
    name: str
    highlight_color_hex: Optional[str] = None

    @field_validator('highlight_color_hex')
    def validate_color_hex(cls, v):
        if v is not None and not v.startswith('#'):
            raise ValueError('Color hex must start with #')
        if v is not None and len(v) != 7:
            raise ValueError('Color hex must be 7 characters long')
        return v

class BillStatusCreate(BillStatusBase):
    pass

class BillStatusUpdate(BillStatusBase):
    archived: Optional[bool] = None

class BillStatusResponse(BillStatusBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class RecurrenceBase(BaseSchema):
    name: str
    calculation: Optional[str] = None

class RecurrenceCreate(RecurrenceBase):
    pass

class RecurrenceUpdate(RecurrenceBase):
    archived: Optional[bool] = None

class RecurrenceResponse(RecurrenceBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class CategoryBase(BaseSchema):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    archived: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class BankAccountBase(BaseSchema):
    name: str
    url: Optional[str] = None
    recurrence: Optional[int] = None
    recurrence_value: Optional[int] = None
    font_color_hex: str

    @field_validator('url')
    def validate_url(cls, v):
        if v is not None and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

    @field_validator('recurrence_value')
    def validate_recurrence_value(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Recurrence value must be greater than 0')
        return v

    @field_validator('font_color_hex')
    def validate_font_color_hex(cls, v):
        if not v.startswith('#'):
            raise ValueError('Color hex must start with #')
        if len(v) != 7:
            raise ValueError('Color hex must be 7 characters long')
        return v

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BankAccountBase):
    archived: Optional[bool] = None

class BankAccountResponse(BankAccountBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class BillBase(BaseSchema):
    name: str
    default_amount_due: Decimal
    url: Optional[str] = None
    default_draft_account: Optional[int] = None
    category: Optional[int] = None
    recurrence: Optional[int] = None
    recurrence_value: Optional[int] = None

    @field_validator('url')
    def validate_url(cls, v):
        if v is not None and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

    @field_validator('recurrence_value')
    def validate_recurrence_value(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Recurrence value must be greater than 0')
        return v

class BillCreate(BillBase):
    pass

class BillUpdate(BillBase):
    archived: Optional[bool] = None

class BillResponse(BillBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class DueBillBase(BaseSchema):
    bill: int
    recurrence: Optional[int] = None
    recurrence_value: Optional[int] = None
    priority: int = 0
    due_date: date
    pay_date: Optional[date] = None
    min_amount_due: Decimal
    total_amount_due: Decimal
    status: Optional[int] = None
    confirmation: Optional[str] = None
    notes: Optional[str] = None
    draft_account: Optional[int] = None

    @field_validator('recurrence_value')
    def validate_recurrence_value(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Recurrence value must be greater than 0')
        return v

class DueBillCreate(DueBillBase):
    pass

class DueBillUpdate(DueBillBase):
    archived: Optional[bool] = None

class DueBillResponse(DueBillBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class BankAccountInstanceBase(BaseSchema):
    bank_account: int
    priority: int = 0
    due_date: date
    pay_date: Optional[date] = None
    status: Optional[int] = None
    current_balance: Decimal

class BankAccountInstanceCreate(BankAccountInstanceBase):
    pass

class BankAccountInstanceUpdate(BankAccountInstanceBase):
    archived: Optional[bool] = None

class BankAccountInstanceResponse(BankAccountInstanceBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class BudgetBase(BaseSchema):
    name: str
    amount: Decimal
    start_date: date
    end_date: date
    category_id: Optional[int] = None

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BudgetBase):
    archived: Optional[bool] = None

class BudgetResponse(BudgetBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class AccountBase(BaseSchema):
    name: str
    balance: Decimal
    account_type: str
    bank_account_id: Optional[int] = None

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    archived: Optional[bool] = None

class AccountResponse(AccountBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime

class TransactionBase(BaseSchema):
    description: str
    amount: Decimal
    transaction_date: date
    account_id: int
    category_id: Optional[int] = None
    budget_id: Optional[int] = None
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    archived: Optional[bool] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: str
    archived: bool
    created_at: datetime
