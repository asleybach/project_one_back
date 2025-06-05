from fastapi import APIRouter
from .income_routes import income_router
from .expense_routes import expense_router
from .balance_routes import balance_router
from .analytics_routes import analytics_router

finance_router = APIRouter(tags=["Finance"])

finance_router.include_router(balance_router)
finance_router.include_router(analytics_router)
finance_router.include_router(income_router)
finance_router.include_router(expense_router)

