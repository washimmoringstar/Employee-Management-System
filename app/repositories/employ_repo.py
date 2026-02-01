from sqlalchemy.orm import Session
from app.db.model import Employee

class EmployRepository:
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Employee).offset(skip).limit(limit).all()

    def create(self, db: Session, employee: Employee):
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee