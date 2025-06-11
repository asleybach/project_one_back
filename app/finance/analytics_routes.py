import calendar
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func
from app.models.expense import Expense
from app.models.income import Income
from app.models.user import User
from app.utils.dependencies import get_db, get_current_user
from calendar import month_name

analytics_router = APIRouter()

@analytics_router.get("/analytics")
def get_analytics(
    year: int = Query(None, description="Año para filtrar"),
    start_date: datetime = Query(None, description="Fecha de inicio (opcional)"),
    end_date: datetime = Query(None, description="Fecha de fin (opcional)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    income_query = db.query(Income).filter(
        Income.user_id == current_user.id,
        Income.is_active == True
    )
    expense_query = db.query(Expense).filter(
        Expense.user_id == current_user.id
    )
    
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

@analytics_router.get("/kpi/monthly", tags=["Finance"])
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
