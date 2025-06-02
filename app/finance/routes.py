from fastapi import APIRouter
from .income_routes import income_router
from .expense_routes import expense_router

finance_router = APIRouter(tags=["Finance"])

finance_router.include_router(income_router)
finance_router.include_router(expense_router)

