from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreateRequest, ExpenseResponse, ExpenseByCategoryResponse, ExpenseListItemResponse
from app.utils.dependencies import get_db, get_current_user
from typing import List

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

@expense_router.put("/expense/{expense_id}", response_model=ExpenseResponse)
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

@expense_router.delete("/expense/{expense_id}")
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

@expense_router.patch("/expense/{expense_id}", response_model=ExpenseResponse)
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

@expense_router.get("/expense/by-category", response_model=List[ExpenseByCategoryResponse])
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


@expense_router.get("/expense/list", response_model=List[ExpenseListItemResponse])
def get_expense_list(
    start_date: datetime = Query(None, description="Fecha de inicio (inclusive)"),
    end_date: datetime = Query(None, description="Fecha de cierre (inclusive)"),
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

from app.schemas.expense import PaginatedExpenseResponse
from app.schemas.income import PaginatedIncomeResponse

@expense_router.get("/expense/paginated_details", response_model=PaginatedExpenseResponse)
def get_all_expenses(
    start_date: datetime = Query(None, description="Fecha de inicio (inclusive)"),
    end_date: datetime = Query(None, description="Fecha de fin (inclusive)"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados por página"),
    offset: int = Query(0, ge=0, description="Número de registros a omitir"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    total = query.count()
    expenses = query.order_by(Expense.date.desc()).offset(offset).limit(limit).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": expenses
    }

