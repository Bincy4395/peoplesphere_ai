
from decimal import Decimal

from sqlalchemy import Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    salary: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False,
        index=True
    )

    # Department relationship
    department: Mapped["Department"] = relationship(
        back_populates="employees"
    )

    # Project relationship
    projects: Mapped[list["Project"]] = relationship(
        secondary="employee_projects",
        back_populates="employees"
    )
