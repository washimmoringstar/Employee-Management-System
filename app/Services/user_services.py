from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.db.model import User
from app.core.sequrity import hash_password # Assuming the typo exists based on user edit history

repo = UserRepository()

class UserService:
    def create_user(self, db: Session, user: UserCreate):
        hashed = hash_password(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed,
            role=user.role,
            is_active=True
        )
        return repo.create(db, db_user)

    def list_users(self, db: Session, skip: int = 0, limit: int = 100):
        return repo.get_all(db, skip, limit)

    def get_user(self, db: Session, user_id: int):
        return repo.get(db, user_id)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        db_user = repo.get(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        
        return repo.update(db, db_user, update_data)

    def delete_user(self, db: Session, user_id: int):
        db_user = repo.get(db, user_id)
        if not db_user:
            return None
        repo.delete(db, db_user)
        return True
