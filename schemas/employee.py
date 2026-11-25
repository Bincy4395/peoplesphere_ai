
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


# Schema for creating an employee
class EmployeeCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=20
    )

    designation: str = Field(
        min_length=2,
        max_length=100
    )

    salary: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    department_id: int = Field(
        gt=0
    )


# Schema for updating an employee
class EmployeeUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        max_length=20
    )

    designation: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    salary: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    department_id: int | None = Field(
        default=None,
        gt=0
    )


# Schema for returning employee data
class EmployeeResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    phone: str | None
    designation: str
    salary: Decimal
    department_id: int

    model_config = ConfigDict(from_attributes=True)
