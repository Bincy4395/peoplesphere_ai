
from pydantic import BaseModel, ConfigDict, Field


# Schema for creating a project
class ProjectCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=150
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )

    status: str = Field(
        default="planned",
        min_length=2,
        max_length=50
    )


# Schema for updating a project
class ProjectUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )

    status: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )


# Schema for returning project data
class ProjectResponse(BaseModel):

    id: int
    name: str
    description: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)
