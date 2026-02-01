from app.db.model import Employee
from app.repositories.employ_repo import EmployRepository


repo = EmployRepository()

class EmployeeService:
    def create_employee(self, db, data):
        employee = Employee(**data.dict())
        return repo.create(db, employee)
    
    def list_employees(self, db, skip, limit):
        return repo.get_all(db, skip, limit)