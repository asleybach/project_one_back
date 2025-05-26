from pydantic import BaseModel
from datetime import datetime
from typing import List

class ExpenseCreateRequest(BaseModel):
    amount: float
    payment_method: str
    category: str
    description: str | None = None
    date: datetime

class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    payment_method: str
    category: str
    description: str | None
    date: datetime
    month: str

    class Config:
        from_attributes = True

class ExpenseByCategoryResponse(BaseModel):
    category: str
    total: float


class ExpenseListItemResponse(BaseModel):
    id: int
    amount: float
    category: str
    date: datetime
    description: str | None
    payment_method: str

    class Config:
        from_attributes = True

class PaginatedExpenseResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[ExpenseResponse]

    class Config:
        from_attributes = True