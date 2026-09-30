from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from services.source_service import add_source
from services.ingestion_service import ingest_text_source


router = APIRouter(
    prefix="/projects",
    tags=["Knowledge Sources"],
)


@router.post("/{project_id}/sources")
async def upload_source(
    project_id: str,
    file: UploadFile = File(...),
):

    temp_directory = Path("temp")

    temp_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_file = temp_directory / file.filename

    content = await file.read()

    temp_file.write_bytes(content)

    source_type = (
        Path(file.filename)
        .suffix
        .lower()
        .replace(".", "")
        or "unknown"
    )

    source = add_source(
        project_id=project_id,
        file_path=str(temp_file),
        source_type=source_type,
        mime_type=file.content_type
        or "application/octet-stream",
    )

    if source_type == "txt":

        ingest_text_source(
            source_id=source.id,
        )

        source_status = "completed"

    else:

        source_status = source.status

    return {
        "id": source.id,
        "project_id": source.project_id,
        "name": source.name,
        "source_type": source.source_type,
        "mime_type": source.mime_type,
        "file_size": source.file_size,
        "status": source_status,
    }


@router.get("/{project_id}/sources")
def list_sources(
    project_id: str,
):

    from database.repository import (
        get_project_knowledge_sources,
    )

    sources = get_project_knowledge_sources(
        project_id
    )

    return [
        {
            "id": source.id,
            "project_id": source.project_id,
            "name": source.name,
            "source_type": source.source_type,
            "mime_type": source.mime_type,
            "file_size": source.file_size,
            "status": source.status,
            "created_at": source.created_at,
        }
        for source in sources
    ]