from sqlalchemy import select
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

async def create_employee(db: AsyncSession, emp: EmployeeCreate):
    db_emp = Employee(
        name=emp.name,
        email=emp.email,
        department_id=emp.department_id
    )
    db.add(db_emp)
    try:
        await db.commit()
        await db.refresh(db_emp)
    except IntegrityError as e:
        await db.rollback()  
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail={"success":False,"message": "Employee with this email already exists", "data":None})
        else:
            raise HTTPException(status_code=400, detail={"success":False,"message": "Database error", "data":None})
    return db_emp

async def get_employees(db: AsyncSession):
    result = await db.execute(
        select(Employee).options(selectinload(Employee.department))
    )
    employees = result.scalars().all()
    return employees

async def update_employee(db: AsyncSession, employee_id: int, emp: EmployeeCreate):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    db_emp = result.scalar_one_or_none()
    
    if not db_emp:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Employee not found", "data": None})
    
    db_emp.name = emp.name
    db_emp.email = emp.email
    db_emp.department_id = emp.department_id
    
    try:
        await db.commit()
        await db.refresh(db_emp)
    except IntegrityError as e:
        await db.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail={"success": False, "message": "Employee with this email already exists", "data": None})
        else:
            raise HTTPException(status_code=400, detail={"success": False, "message": "Database error", "data": None})
    
    return db_emp

async def delete_employee(db: AsyncSession, employee_id: int):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    db_emp = result.scalar_one_or_none()
    
    if not db_emp:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Employee not found", "data": None})
    
    await db.delete(db_emp)
    await db.commit()
    
    return {"success": True, "message": "Employee deleted successfully"}