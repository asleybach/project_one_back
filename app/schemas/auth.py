from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    username: str  
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr  
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    is_admin: bool