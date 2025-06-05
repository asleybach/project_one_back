from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreateRequest, ExpenseResponse
from app.schemas.income import IncomeCreateRequest, IncomeResponse
from app.utils.dependencies import get_db, get_current_user

balance_router = APIRouter()

@balance_router.get("/balance")
def get_balance(
    day: int = Query(None, ge=1, le=31),
    month: int = Query(None, ge=1, le=12),
    year: int = Query(None, ge=1900),
    start_date: datetime = Query(None, description="Fecha de inicio (inclusive)"),
    end_date: datetime = Query(None, description="Fecha de fin (inclusive)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    filters = [Income.user_id == current_user.id]
    expense_filters = [Expense.user_id == current_user.id]

    if start_date:
        filters.append(Income.date >= start_date)
        expense_filters.append(Expense.date >= start_date)
    if end_date:
        filters.append(Income.date <= end_date)
        expense_filters.append(Expense.date <= end_date)

    if not start_date and not end_date:
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
        "filters": {
            "day": day,
            "month": month,
            "year": year,
            "start_date": start_date,
            "end_date": end_date
        }
    }
