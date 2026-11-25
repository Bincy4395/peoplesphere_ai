
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.employee import Employee
from models.department import Department

from schemas.employee import EmployeeCreate, EmployeeUpdate

from repositories import employee_repository


# Get all employees
def get_all_employees(db: Session):

    return employee_repository.get_all_employees(db)


# Get employee by ID
def get_employee_by_id(db: Session, employee_id: int):

    employee = employee_repository.get_employee_by_id(
        db, employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return employee


# Create employee
def create_employee(db: Session, employee_data: EmployeeCreate):

    # Check duplicate email
    existing_employee = db.query(Employee).filter(
        Employee.email == employee_data.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee email already exists"
        )

    # Check department exists
    department = db.query(Department).filter(
        Department.id == employee_data.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    return employee_repository.create_employee(
        db, employee_data
    )


# Update employee
def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):

    employee = get_employee_by_id(db, employee_id)

    update_data = employee_data.model_dump(exclude_unset=True)

    # Check duplicate email
    if "email" in update_data:
        existing_employee = db.query(Employee).filter(
            Employee.email == update_data["email"],
            Employee.id != employee_id
        ).first()

        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee email already exists"
            )

    # Check department exists
    if "department_id" in update_data:
        department = db.query(Department).filter(
            Department.id == update_data["department_id"]
        ).first()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

    return employee_repository.update_employee(
        db, employee, employee_data
    )


# Delete employee
def delete_employee(db: Session, employee_id: int):

    employee = get_employee_by_id(db, employee_id)

    employee_repository.delete_employee(db, employee)

    return {"message": "Employee deleted successfully"}
