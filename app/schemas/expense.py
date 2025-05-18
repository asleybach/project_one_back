from pydantic import BaseModel
from datetime import datetime

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