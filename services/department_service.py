
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.department import Department
from schemas.department import DepartmentCreate, DepartmentUpdate
from repositories import department_repository


# Get all departments
def get_all_departments(db: Session):

    return department_repository.get_all_departments(db)


# Get department by ID
def get_department_by_id(db: Session, department_id: int):

    department = department_repository.get_department_by_id(
        db, department_id
    )

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    return department


# Create department
def create_department(db: Session, department_data: DepartmentCreate):

    existing_department = db.query(Department).filter(
        Department.name == department_data.name
    ).first()

    if existing_department:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department already exists"
        )

    return department_repository.create_department(
        db, department_data
    )


# Update department
def update_department(
    db: Session,
    department_id: int,
    department_data: DepartmentUpdate
):

    department = get_department_by_id(db, department_id)

    update_data = department_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_department = db.query(Department).filter(
            Department.name == update_data["name"],
            Department.id != department_id
        ).first()

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department name already exists"
            )

    return department_repository.update_department(
        db, department, department_data
    )


# Delete department
def delete_department(db: Session, department_id: int):

    department = get_department_by_id(db, department_id)

    department_repository.delete_department(db, department)

    return {"message": "Department deleted successfully"}
