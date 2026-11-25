
from pydantic import BaseModel, ConfigDict, Field


# Schema for creating a department
class DepartmentCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


# Schema for updating a department
class DepartmentUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


# Schema for returning department data
class DepartmentResponse(BaseModel):

    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)
