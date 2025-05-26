from pydantic import BaseModel
from datetime import datetime
from typing import List

class IncomeCreateRequest(BaseModel):
    source: str
    amount: float
    observations: str | None = None
    date: datetime

class IncomeResponse(BaseModel):
    id: int
    user_id: int
    source: str
    amount: float
    observations: str | None
    date: datetime
    month: str

    class Config:
        from_attributes = True

class PaginatedIncomeResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[IncomeResponse]

    class Config:
        from_attributes = True