from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.income import Income
from app.models.expense import Expense
from app.schemas.user import UserCreateRequest, UserResponse
from app.utils.dependencies import get_db, get_current_user
from typing import List, Optional

admin_router = APIRouter(tags=["Admin"])

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user

@admin_router.get("/admin/users", response_model=List[UserResponse])
def get_all_users(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Ejemplo de consumo desde el frontend:

    Todos: /admin/users
    Solo activos: /admin/users?is_active=true
    Solo inactivos: /admin/users?is_active=false
    """
    query = db.query(User)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()

@admin_router.post("/admin/users", response_model=UserResponse)
def create_user(
    user: UserCreateRequest,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@admin_router.put("/admin/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserCreateRequest,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@admin_router.delete("/admin/users/{user_id}")
def inactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user.is_active = False
    db.query(Income).filter(Income.user_id == user_id).update({"is_active": False})
    db.query(Expense).filter(Expense.user_id == user_id).update({"is_active": False})

    db.commit()
    return {"detail": "Usuario y registros asociados inactivados correctamente"}