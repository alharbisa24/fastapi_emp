from pydantic import BaseModel, EmailStr
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.department import DepartmentOutForEmployee

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr

class EmployeeCreate(EmployeeBase):
    department_id: int

class EmployeeOut(EmployeeBase):
    id: int
    department: Optional["DepartmentOutForEmployee"] = None 

    class Config:
        orm_mode = True

from app.schemas.department import DepartmentOutForEmployee
EmployeeOut.model_rebuild()