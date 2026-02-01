from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, check_permission
from app.Services.user_services import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.db.model import User

router = APIRouter(prefix="/users", tags=["users"])
services = UserService()

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("user: create"))
):
    try:
        return services.create_user(db, user_data)
    except Exception as e:
        # Simple error handling for duplicate email or other issues
        if "UNIQUE constraint failed" in str(e) or "IntegrityError" in str(e):
             raise HTTPException(status_code=400, detail="User with this email already exists.")
        raise e

@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("user: read"))
):
    return services.list_users(db, skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("user: read"))
):
    user = services.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("user: update"))
):
    user = services.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("user: delete"))
):
    success = services.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
