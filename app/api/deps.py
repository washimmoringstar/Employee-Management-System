from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import sessionlocal
from app.db.model import Base, User 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# -----------------------
# Database Dependency
# -----------------------
def get_db() -> Generator[Session, None, None]:
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------
# Auth Dependencies
# -----------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    return user
# -----------------------
# Permissions
# -----------------------

def require_permission(
    permission: str,
    current_user: User = Depends(get_current_user),
) -> User:
    if permission not in role_permissions.get(current_user.role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    return current_user

# -----------------------
# Role-Based Access
# -----------------------
def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


def require_hr_or_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in {"admin", "hr"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HR or Admin privileges required",
        )
    return current_user


# -----------------------
# Permissions
# -----------------------
from app.core.permissions import role_permissions

def check_permission(permission: str):
    def dependency(current_user: User = Depends(get_current_user)):
        if permission not in role_permissions.get(current_user.role, []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )
        return current_user
    return dependency
