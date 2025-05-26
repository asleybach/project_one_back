from pydantic import BaseModel
from datetime import datetime

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