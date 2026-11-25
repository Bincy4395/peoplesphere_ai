
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db

from schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)
from services import department_service


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# Get all departments
@router.get(
    "/",
    response_model=list[DepartmentResponse]
)
def get_all_departments(db: Session = Depends(get_db)):

    return department_service.get_all_departments(db)


# Get department by ID
@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department_by_id(
    department_id: int,
    db: Session = Depends(get_db)
):

    return department_service.get_department_by_id(
        db, department_id
    )


# Create department
@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db)
):

    return department_service.create_department(
        db, department_data
    )


# Update department
@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db)
):

    return department_service.update_department(
        db, department_id, department_data
    )


# Delete department
@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    return department_service.delete_department(
        db, department_id
    )
