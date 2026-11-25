
from sqlalchemy.orm import Session

from models.department import Department
from schemas.department import DepartmentCreate, DepartmentUpdate


# Get all departments
def get_all_departments(db: Session):

    return db.query(Department).all()


# Get department by ID
def get_department_by_id(db: Session, department_id: int):

    return db.query(Department).filter(
        Department.id == department_id
    ).first()


# Create department
def create_department(db: Session, department_data: DepartmentCreate):

    department = Department(
        name=department_data.name,
        description=department_data.description
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


# Update department
def update_department(
    db: Session,
    department: Department,
    department_data: DepartmentUpdate
):

    update_data = department_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


# Delete department
def delete_department(db: Session, department: Department):

    db.delete(department)
    db.commit()

    return True
