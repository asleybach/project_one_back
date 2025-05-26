from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.auth.jwt_handler import create_access_token
from app.models.user import User
from app.database.database import SessionLocal
import bcrypt

auth_router = APIRouter(tags=["Auth"])  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not bcrypt.checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username
    )

@auth_router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    
    user = db.query(User).filter((User.username == request.username) | (User.email == request.email)).first()
    if user:
        raise HTTPException(status_code=400, detail="Username or email already exists")    
    
    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())    
    new_user = User(username=request.username, email=request.email, password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    access_token = create_access_token({"sub": new_user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        username=new_user.username
    )