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
