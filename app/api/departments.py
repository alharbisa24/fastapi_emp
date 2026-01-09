from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentOut
from app.services import department_service
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import current_active_user

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentOut)
async def create_department(dept: DepartmentCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    return await department_service.create_department(db, dept)

@router.get("/", response_model=list[DepartmentOut])
async def get_departments(db: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    return await department_service.get_departments(db)

@router.put("/{department_id}", response_model=DepartmentOut)
async def update_department(
    department_id: int,
    dept: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    return await department_service.update_department(db, department_id, dept)

@router.delete("/{department_id}")
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    await department_service.delete_department(db, department_id)
    return {"message": "Department deleted successfully"}