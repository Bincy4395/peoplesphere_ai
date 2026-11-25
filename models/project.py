
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


# Association table
employee_projects = Table(
    "employee_projects",
    Base.metadata,

    Column(
        "employee_id",
        Integer,
        ForeignKey("employees.id"),
        primary_key=True
    ),

    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id"),
        primary_key=True
    )
)


class Project(Base):

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="planned",
        nullable=False
    )

    employees: Mapped[list["Employee"]] = relationship(
        secondary=employee_projects,
        back_populates="projects"
    )
