from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeBase, EmployeeOut
from app.services import employee_service
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.auth import current_active_user

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeBase)
async def create_employee(emp: EmployeeCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    return await employee_service.create_employee(db, emp)


@router.get("/", response_model=List[EmployeeOut])
async def get_employees(db: AsyncSession = Depends(get_db),  user: User = Depends(current_active_user)):
    employees = await employee_service.get_employees(db)
    return employees


@router.put("/{employee_id}", response_model=EmployeeOut)
async def update_employee(
    employee_id: int,
    emp: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    return await employee_service.update_employee(db, employee_id, emp)


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    await employee_service.delete_employee(db, employee_id)
    return {"message": "Employee deleted successfully"}