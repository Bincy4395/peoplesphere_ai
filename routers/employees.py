
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db

from schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)

from services import employee_service


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# Get all employees
@router.get(
    "/",
    response_model=list[EmployeeResponse]
)
def get_all_employees(
    db: Session = Depends(get_db)
):

    return employee_service.get_all_employees(db)


# Get employee by ID
@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db)
):

    return employee_service.get_employee_by_id(
        db, employee_id
    )


# Create employee
@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    return employee_service.create_employee(
        db, employee_data
    )


# Update employee
@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    return employee_service.update_employee(
        db, employee_id, employee_data
    )


# Delete employee
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    return employee_service.delete_employee(
        db, employee_id
    )
