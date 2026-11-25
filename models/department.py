
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Department(Base):

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department"
    )
