
from sqlalchemy.orm import Session

from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate


# Get all employees
def get_all_employees(db: Session):

    return db.query(Employee).all()


# Get employee by ID
def get_employee_by_id(db: Session, employee_id: int):

    return db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


# Create employee
def create_employee(db: Session, employee_data: EmployeeCreate):

    employee = Employee(
        **employee_data.model_dump()
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# Update employee
def update_employee(
    db: Session,
    employee: Employee,
    employee_data: EmployeeUpdate
):

    update_data = employee_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


# Delete employee
def delete_employee(db: Session, employee: Employee):

    db.delete(employee)
    db.commit()

    return True
