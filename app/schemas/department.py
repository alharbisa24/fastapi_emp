from pydantic import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.employee import EmployeeOut  

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    employees: List["EmployeeOut"] = []  


class DepartmentOutForEmployee(DepartmentBase):
    id: int

class Config:
    orm_mode = True

from app.schemas.employee import EmployeeOut
DepartmentOut.model_rebuild()