from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_hr_or_admin
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.Services.employee_services import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])

services = EmployeeService()

@router.post("/", response_model=EmployeeResponse)
def create_employee( 
    payload: EmployeeCreate,
    db : Session = Depends(get_db),
    current_user = Depends(require_hr_or_admin)
):
    try:
        return services.create_employee(db, payload)
    except Exception as e:
        # Check for integrity error (duplicate entry)
        if "UNIQUE constraint failed" in str(e) or "IntegrityError" in str(e):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Employee with this email already exists.")
        raise e

@router.get("/", response_model=list[EmployeeResponse])
def list_employees(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(require_hr_or_admin)
):
    return services.list_employees(db, skip, limit)