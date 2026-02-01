from pydantic import BaseModel,EmailStr

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    position: str
    salary: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True