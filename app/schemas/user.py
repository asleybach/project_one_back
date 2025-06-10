from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True