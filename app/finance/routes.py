from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreateRequest, IncomeResponse
from app.auth.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer

finance_router = APIRouter()

# Configuración para obtener el token de autorización
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencia para validar el token y obtener el usuario
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@finance_router.post("/income", response_model=IncomeResponse)
def create_income(
    request: IncomeCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Crear un nuevo ingreso
    new_income = Income(
        user_id=current_user.id,
        source=request.source,
        amount=request.amount,
        category=request.category,
        observations=request.observations,
        date=request.date,
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return new_income