from fastapi import APIRouter
from pydantic import BaseModel

from database.repository import (
    create_project,
    get_projects,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None


@router.post("/")
def create_new_project(
    request: CreateProjectRequest,
):
    project = create_project(
        name=request.name,
        description=request.description,
    )

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at,
    }


@router.get("/")
def list_projects():

    projects = get_projects()

    return [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
        }
        for project in projects
    ]