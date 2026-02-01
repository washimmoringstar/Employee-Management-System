from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.Services.auth_services import AuthService
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()
user_repo = UserRepository()

@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth_service.get_password_hash(user.password)
    user.password = hashed_password
    
    # Create User object here to map schema to model
    from app.db.model import User
    new_user = User(email=user.email, hashed_password=hashed_password, role="staff", is_active=True)
    
    return user_repo.create(db, new_user)

@router.post("/login", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"DEBUG: Login attempt for username: '{form_data.username}'")
    print(f"DEBUG: Password received: '{form_data.password}'")
    
    user = user_repo.get_by_email(db, email=form_data.username)
    
    if user:
        print(f"DEBUG: User found: {user.email}, Role: {user.role}, Hash: {user.hashed_password[:10]}...")
        is_password_valid = auth_service.verify_password(form_data.password, user.hashed_password)
        print(f"DEBUG: Password valid? {is_password_valid}")
    else:
        print("DEBUG: User not found in DB")

    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
