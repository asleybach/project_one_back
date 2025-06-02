from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreateRequest, ExpenseResponse
from app.utils.dependencies import get_db, get_current_user

expense_router = APIRouter()

@expense_router.post("/expense", response_model=ExpenseResponse)
def create_expense(
    request: ExpenseCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

@expense_router.get("/expense", response_model=list[ExpenseResponse])
def get_all_expenses(
    start_date: datetime = Query(None, description="Fecha de inicio (inclusive)"),
    end_date: datetime = Query(None, description="Fecha de fin (inclusive)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    expenses = query.order_by(Expense.date.desc()).all()
    return expenses
