
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)
from services import project_service


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# Get all projects
@router.get("/", response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    return project_service.get_all_projects(db)


# Get project by ID
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db)
):
    return project_service.get_project_by_id(db, project_id)


# Create project
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    return project_service.create_project(db, project_data)


# Update project
@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    return project_service.update_project(
        db, project_id, project_data
    )


# Delete project
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    return project_service.delete_project(db, project_id)


# Assign employee to project
@router.post("/{project_id}/employees/{employee_id}")
def assign_employee_to_project(
    project_id: int,
    employee_id: int,
    db: Session = Depends(get_db)
):
    return project_service.assign_employee_to_project(
        db,
        project_id,
        employee_id
    )


# Remove employee from project
@router.delete("/{project_id}/employees/{employee_id}")
def remove_employee_from_project(
    project_id: int,
    employee_id: int,
    db: Session = Depends(get_db)
):
    return project_service.remove_employee_from_project(
        db,
        project_id,
        employee_id
    )
