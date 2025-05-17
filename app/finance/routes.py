from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreateRequest, IncomeResponse
from app.auth.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreateRequest, ExpenseResponse, ExpenseByCategoryResponse
from sqlalchemy import func
from typing import List, Dict

finance_router = APIRouter(tags=["Finance"])  # Agregar etiqueta "Finance"

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

# Obtener todos los ingresos del usuario actual
@finance_router.get("/income", response_model=list[IncomeResponse])
def get_all_incomes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    incomes = db.query(Income).filter(Income.user_id == current_user.id).all()
    return incomes

# Actualizar un ingreso existente (PUT)
@finance_router.put("/income/{income_id}", response_model=IncomeResponse)
def update_income(
    income_id: int,
    request: IncomeCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    income = db.query(Income).filter(Income.id == income_id, Income.user_id == current_user.id).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    income.source = request.source
    income.amount = request.amount
    income.category = request.category
    income.observations = request.observations
    income.date = request.date
    db.commit()
    db.refresh(income)
    return income

# Eliminar un ingreso existente (DELETE)
@finance_router.delete("/income/{income_id}")
def delete_income(
    income_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    income = db.query(Income).filter(Income.id == income_id, Income.user_id == current_user.id).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    db.delete(income)
    db.commit()
    return {"detail": "Income deleted successfully"}

# Actualizar parcialmente un ingreso existente (PATCH)
@finance_router.patch("/income/{income_id}", response_model=IncomeResponse)
def patch_income(
    income_id: int,
    request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    income = db.query(Income).filter(Income.id == income_id, Income.user_id == current_user.id).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    for key, value in request.items():
        if hasattr(income, key):
            setattr(income, key, value)

    db.commit()
    db.refresh(income)
    return income

@finance_router.post("/expense", response_model=ExpenseResponse)
def create_expense(
    request: ExpenseCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Crear un nuevo gasto
    new_expense = Expense(
        user_id=current_user.id,
        amount=request.amount,
        payment_method=request.payment_method,
        category=request.category,
        description=request.description,
        date=request.date,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

# Obtener todos los gastos del usuario actual
@finance_router.get("/expense", response_model=list[ExpenseResponse])
def get_all_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expenses

# Actualizar un gasto existente (PUT)
@finance_router.put("/expense/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    request: ExpenseCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = request.amount
    expense.payment_method = request.payment_method
    expense.category = request.category
    expense.description = request.description
    expense.date = request.date
    db.commit()
    db.refresh(expense)
    return expense

# Eliminar un gasto existente (DELETE)
@finance_router.delete("/expense/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"detail": "Expense deleted successfully"}

# Actualizar parcialmente un gasto existente (PATCH)
@finance_router.patch("/expense/{expense_id}", response_model=ExpenseResponse)
def patch_expense(
    expense_id: int,
    request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for key, value in request.items():
        if hasattr(expense, key):
            setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense

@finance_router.get("/balance")
def get_balance(
    day: int = Query(None, ge=1, le=31),
    month: int = Query(None, ge=1, le=12),
    year: int = Query(None, ge=1900),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    filters = [Income.user_id == current_user.id]
    expense_filters = [Expense.user_id == current_user.id]

    if year is not None:
        filters.append(func.extract('year', Income.date) == year)
        expense_filters.append(func.extract('year', Expense.date) == year)
    if month is not None:
        filters.append(func.extract('month', Income.date) == month)
        expense_filters.append(func.extract('month', Expense.date) == month)
    if day is not None:
        filters.append(func.extract('day', Income.date) == day)
        expense_filters.append(func.extract('day', Expense.date) == day)

    total_income = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(*filters).scalar()
    total_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(*expense_filters).scalar()
    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "filters": {"day": day, "month": month, "year": year}
    }

@finance_router.get("/expense/by-category", response_model=List[ExpenseByCategoryResponse])
def get_expense_by_category(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = (
        db.query(Expense.category, func.sum(Expense.amount).label("total"))
        .filter(Expense.user_id == current_user.id)
        .group_by(Expense.category)
        .all()
    )
    return [{"category": category, "total": float(total)} for category, total in results]