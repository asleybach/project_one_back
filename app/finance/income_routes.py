from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreateRequest, IncomeResponse
from app.utils.dependencies import get_db, get_current_user

income_router = APIRouter()

@income_router.post("/income", response_model=IncomeResponse)
def create_income(
    request: IncomeCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_income = Income(
        user_id=current_user.id,
        source=request.source,
        amount=request.amount,
        observations=request.observations,
        date=request.date,
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income

@income_router.get("/income", response_model=list[IncomeResponse])
def get_all_incomes(
    start_date: datetime = Query(None, description="Fecha de inicio (inclusive)"),
    end_date: datetime = Query(None, description="Fecha de fin (inclusive)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Income).filter(Income.user_id == current_user.id)
    if start_date:
        query = query.filter(Income.date >= start_date)
    if end_date:
        query = query.filter(Income.date <= end_date)
    incomes = query.order_by(Income.date.desc()).all()
    return incomes

@income_router.put("/income/{income_id}", response_model=IncomeResponse)
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

@income_router.delete("/income/{income_id}")
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

@income_router.patch("/income/{income_id}", response_model=IncomeResponse)
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
@income_router.get("/income/paginated_details", response_model=PaginatedIncomeResponse)
def get_all_incomes(
    start_date: datetime = Query(None, description="Fecha de inicio (inclusive)"),
    end_date: datetime = Query(None, description="Fecha de fin (inclusive)"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados por página"),
    offset: int = Query(0, ge=0, description="Número de registros a omitir"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Income).filter(Income.user_id == current_user.id)
    if start_date:
        query = query.filter(Income.date >= start_date)
    if end_date:
        query = query.filter(Income.date <= end_date)
    total = query.count()
    incomes = query.order_by(Income.date.desc()).offset(offset).limit(limit).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": incomes
    }
