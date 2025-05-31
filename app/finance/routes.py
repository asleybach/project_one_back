from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreateRequest, IncomeResponse
from app.auth.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreateRequest, ExpenseResponse, ExpenseByCategoryResponse, ExpenseListItemResponse, PaginatedExpenseResponse
from sqlalchemy import func
from typing import List, Dict
from datetime import datetime
import calendar
from calendar import month_name

finance_router = APIRouter(tags=["Finance"])  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@finance_router.get("/income", response_model=list[IncomeResponse])
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

@finance_router.get("/expense", response_model=list[ExpenseResponse])
def get_all_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expenses

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


@finance_router.get("/expense/list", response_model=List[ExpenseListItemResponse])
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

@finance_router.get("/expense/paginated_details", response_model=PaginatedExpenseResponse)
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

@finance_router.get("/income/paginated_details", response_model=PaginatedIncomeResponse)
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

@finance_router.get("/analytics")
def get_analytics(
    year: int = Query(None, description="Año para filtrar"),
    start_date: datetime = Query(None, description="Fecha de inicio (opcional)"),
    end_date: datetime = Query(None, description="Fecha de fin (opcional)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    income_query = db.query(Income).filter(Income.user_id == current_user.id)
    expense_query = db.query(Expense).filter(Expense.user_id == current_user.id)
    
    if year:
        income_query = income_query.filter(func.extract('year', Income.date) == year)
        expense_query = expense_query.filter(func.extract('year', Expense.date) == year)
    if start_date:
        income_query = income_query.filter(Income.date >= start_date)
        expense_query = expense_query.filter(Expense.date >= start_date)
    if end_date:
        income_query = income_query.filter(Income.date <= end_date)
        expense_query = expense_query.filter(Expense.date <= end_date)

    total_income = income_query.with_entities(func.coalesce(func.sum(Income.amount), 0)).scalar()
    total_expense = expense_query.with_entities(func.coalesce(func.sum(Expense.amount), 0)).scalar()
    monthly_balance = total_income - total_expense
    savings = monthly_balance
    savings_percent = round((savings / total_income * 100), 2) if total_income else 0

    expenses_by_category = [
        {"category": c, "total": float(t)}
        for c, t in db.query(Expense.category, func.sum(Expense.amount))
            .filter(Expense.user_id == current_user.id)
            .group_by(Expense.category)
            .all()
    ]

    income_by_category = [
        {"category": c, "total": float(t)}
        for c, t in db.query(Income.source, func.sum(Income.amount))
            .filter(Income.user_id == current_user.id)
            .group_by(Income.source)
            .all()
    ]

    expenses_by_month = [
        {
            "month": f"{int(y):04d}-{int(m):02d}",
            "monthName": f"{calendar.month_name[int(m)]} {int(y)}",
            "total": float(t)
        }
        for y, m, t in db.query(
            func.extract('year', Expense.date),
            func.extract('month', Expense.date),
            func.sum(Expense.amount)
        )
        .filter(Expense.user_id == current_user.id)
        .group_by(func.extract('year', Expense.date), func.extract('month', Expense.date))
        .order_by(func.extract('year', Expense.date), func.extract('month', Expense.date))
        .all()
    ]

    income_by_month = [
        {
            "month": f"{int(y):04d}-{int(m):02d}",
            "monthName": f"{calendar.month_name[int(m)]} {int(y)}",
            "total": float(t)
        }
        for y, m, t in db.query(
            func.extract('year', Income.date),
            func.extract('month', Income.date),
            func.sum(Income.amount)
        )
        .filter(Income.user_id == current_user.id)
        .group_by(func.extract('year', Income.date), func.extract('month', Income.date))
        .order_by(func.extract('year', Income.date), func.extract('month', Income.date))
        .all()
    ]

    income_month_dict = {item["month"]: item["total"] for item in income_by_month}
    expense_month_dict = {item["month"]: item["total"] for item in expenses_by_month}
    all_months = sorted(set(list(income_month_dict.keys()) + list(expense_month_dict.keys())))
    monthly_balances = [
        income_month_dict.get(month, 0) - expense_month_dict.get(month, 0)
        for month in all_months
    ]

    pareto_data = sorted(expenses_by_category, key=lambda x: x["total"], reverse=True)
    cumulative = 0
    total = sum(x["total"] for x in pareto_data) or 1
    expenses_pareto = []
    for item in pareto_data:
        cumulative += item["total"]
        expenses_pareto.append({
            "category": item["category"],
            "total": item["total"],
            "cumulativePercent": round(cumulative / total * 100, 1)
        })

    ranges = [(0, 100), (101, 500), (501, 1000)]
    expenses_distribution = []
    for r in ranges:
        count = db.query(func.count(Expense.id)).filter(
            Expense.user_id == current_user.id,
            Expense.amount >= r[0],
            Expense.amount <= r[1]
        ).scalar()
        expenses_distribution.append({
            "amountRange": f"{r[0]}-{r[1]}",
            "count": count
        })

    pivot_table = [
        {"month": f"{int(y):04d}-{int(m):02d}", "category": c, "total": float(t)}
        for y, m, c, t in db.query(
            func.extract('year', Expense.date),
            func.extract('month', Expense.date),
            Expense.category,
            func.sum(Expense.amount)
        )
        .filter(Expense.user_id == current_user.id)
        .group_by(func.extract('year', Expense.date), func.extract('month', Expense.date), Expense.category)
        .order_by(func.extract('year', Expense.date), func.extract('month', Expense.date), Expense.category)
        .all()
    ]

    selected_year = year if year else datetime.now().year
    all_months = [f"{selected_year:04d}-{m:02d}" for m in range(1, 13)]
    all_month_names = [f"{calendar.month_name[m]} {selected_year}" for m in range(1, 13)]

    expenses_by_month_raw = {
        f"{int(y):04d}-{int(m):02d}": float(t)
        for y, m, t in db.query(
            func.extract('year', Expense.date),
            func.extract('month', Expense.date),
            func.sum(Expense.amount)
        )
        .filter(
            Expense.user_id == current_user.id,
            func.extract('year', Expense.date) == selected_year
        )
        .group_by(func.extract('year', Expense.date), func.extract('month', Expense.date))
        .all()
    }

    income_by_month_raw = {
        f"{int(y):04d}-{int(m):02d}": float(t)
        for y, m, t in db.query(
            func.extract('year', Income.date),
            func.extract('month', Income.date),
            func.sum(Income.amount)
        )
        .filter(
            Income.user_id == current_user.id,
            func.extract('year', Income.date) == selected_year
        )
        .group_by(func.extract('year', Income.date), func.extract('month', Income.date))
        .all()
    }

    expenses_by_month = [
        {
            "month": month,
            "monthName": month_name,
            "total": expenses_by_month_raw.get(month, 0)
        }
        for month, month_name in zip(all_months, all_month_names)
    ]

    income_by_month = [
        {
            "month": month,
            "monthName": month_name,
            "total": income_by_month_raw.get(month, 0)
        }
        for month, month_name in zip(all_months, all_month_names)
    ]

    monthly_balances = [
        income_by_month[i]["total"] - expenses_by_month[i]["total"]
        for i in range(12)
    ]

    return {
        "kpis": {
            "monthlyBalance": monthly_balance,
            "totalIncome": total_income,
            "totalExpense": total_expense,
            "savings": savings,
            "savingsPercent": savings_percent
        },
        "monthlyBalances": monthly_balances,
        "expensesByCategory": expenses_by_category,
        "incomeByCategory": income_by_category,
        "expensesByMonth": expenses_by_month,
        "incomeByMonth": income_by_month,
        "expensesPareto": expenses_pareto,
        "expensesDistribution": expenses_distribution,
        "pivotTable": pivot_table
    }

@finance_router.get("/kpi/monthly", tags=["Finance"])
def get_monthly_kpis(
    year: int = Query(None, description="Año a consultar"),
    month: int = Query(None, ge=1, le=12, description="Mes a consultar (1=Enero, 12=Diciembre)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    selected_year = year if year else datetime.now().year
    selected_month = month if month else datetime.now().month

    income_query = db.query(Income).filter(
        Income.user_id == current_user.id,
        func.extract('year', Income.date) == selected_year,
        func.extract('month', Income.date) == selected_month
    )
    
    expense_query = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        func.extract('year', Expense.date) == selected_year,
        func.extract('month', Expense.date) == selected_month
    )
    
    total_income = income_query.with_entities(func.coalesce(func.sum(Income.amount), 0)).scalar()
    total_expense = expense_query.with_entities(func.coalesce(func.sum(Expense.amount), 0)).scalar()
    monthly_balance = total_income - total_expense
    savings = monthly_balance
    savings_percent = round((savings / total_income * 100), 2) if total_income else 0

    # Expenses by category para el mes filtrado
    expenses_by_category = [
        {"category": c, "total": float(t)}
        for c, t in db.query(Expense.category, func.sum(Expense.amount))
            .filter(
                Expense.user_id == current_user.id,
                func.extract('year', Expense.date) == selected_year,
                func.extract('month', Expense.date) == selected_month
            )
            .group_by(Expense.category)
            .all()
    ]

    return {
        "year": selected_year,
        "month": selected_month,
        "monthName": f"{month_name[selected_month]} {selected_year}",
        "monthlyBalance": monthly_balance,
        "totalIncome": total_income,
        "totalExpense": total_expense,
        "savings": savings,
        "savingsPercent": savings_percent,
        "expensesByCategory": expenses_by_category
    }
