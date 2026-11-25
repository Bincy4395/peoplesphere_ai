
from sqlalchemy.orm import Session

from models.project import Project
from schemas.project import ProjectCreate, ProjectUpdate


# Get all projects
def get_all_projects(db: Session):

    return db.query(Project).all()


# Get project by ID
def get_project_by_id(db: Session, project_id: int):

    return db.query(Project).filter(
        Project.id == project_id
    ).first()


# Create project
def create_project(db: Session, project_data: ProjectCreate):

    project = Project(
        **project_data.model_dump()
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# Update project
def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate
):

    update_data = project_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


# Delete project
def delete_project(db: Session, project: Project):

    db.delete(project)
    db.commit()

    return True
