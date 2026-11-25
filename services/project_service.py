
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.project import Project
from models.employee import Employee

from schemas.project import ProjectCreate, ProjectUpdate

from repositories import project_repository


# Get all projects
def get_all_projects(db: Session):

    return project_repository.get_all_projects(db)


# Get project by ID
def get_project_by_id(db: Session, project_id: int):

    project = project_repository.get_project_by_id(
        db, project_id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project


# Create project
def create_project(db: Session, project_data: ProjectCreate):

    existing_project = db.query(Project).filter(
        Project.name == project_data.name
    ).first()

    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project name already exists"
        )

    return project_repository.create_project(
        db, project_data
    )


# Update project
def update_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate
):

    project = get_project_by_id(db, project_id)

    update_data = project_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_project = db.query(Project).filter(
            Project.name == update_data["name"],
            Project.id != project_id
        ).first()

        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project name already exists"
            )

    return project_repository.update_project(
        db, project, project_data
    )


# Delete project
def delete_project(db: Session, project_id: int):

    project = get_project_by_id(db, project_id)

    project_repository.delete_project(db, project)

    return {"message": "Project deleted successfully"}



def assign_employee_to_project(
    db: Session,
    project_id: int,
    employee_id: int
):
    project = get_project_by_id(db, project_id)

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    if employee in project.employees:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee is already assigned to this project"
        )

    project.employees.append(employee)

    db.commit()
    db.refresh(project)

    return {
        "message": "Employee assigned to project successfully"
    }



def remove_employee_from_project(
    db: Session,
    project_id: int,
    employee_id: int
):
    project = get_project_by_id(db, project_id)

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    if employee not in project.employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee is not assigned to this project"
        )

    project.employees.remove(employee)

    db.commit()

    return {
        "message": "Employee removed from project successfully"
    }
