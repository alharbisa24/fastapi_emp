from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department import Department
from app.schemas.department import DepartmentCreate
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

async def create_department(db: AsyncSession, dept: DepartmentCreate):
    db_dept = Department(name=dept.name)
    db.add(db_dept)
    try:
        await db.commit()
        await db.refresh(db_dept)
    except IntegrityError as e:
        await db.rollback()  
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail={"success":False,"message": "Department with entered name already exists", "data":None})
        else:
            raise HTTPException(status_code=400, detail={"success":False,"message": "Database error", "data":None})
        
    result = await db.execute(
        select(Department)
        .options(selectinload(Department.employees))
        .where(Department.id == db_dept.id)
    )
    db_dept = result.scalars().first()

    return db_dept


async def get_departments(db: AsyncSession):
    result = await db.execute(
        select(Department).options(selectinload(Department.employees))
    )
    return result.scalars().all()


async def update_department(db: AsyncSession, dept_id: int, dept: DepartmentCreate):
    result = await db.execute(
        select(Department).where(Department.id == dept_id)
    )
    db_dept = result.scalars().first()
    if db_dept:
        db_dept.name = dept.name
        await db.commit()
        await db.refresh(db_dept)
        result = await db.execute(
            select(Department)
            .options(selectinload(Department.employees))
            .where(Department.id == dept_id)
        )
        db_dept = result.scalars().first()
    return db_dept


async def delete_department(db: AsyncSession, dept_id: int):
    result = await db.execute(
        select(Department).where(Department.id == dept_id)
    )
    db_dept = result.scalars().first()
    if db_dept:
        await db.delete(db_dept)
        await db.commit()
    return db_dept