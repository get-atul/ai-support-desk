from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    UploadFile,
)
from fastapi.responses import FileResponse

from database.repository import (
    get_knowledge_source,
)
from services.source_service import add_source
from services.ingestion_service import (
    ingest_source,
)


router = APIRouter(
    prefix="/projects",
    tags=["Knowledge Sources"],
)


SUPPORTED_TYPES = {
    "txt",
    "pdf",
    "docx",
    "mp3",
    "wav",
    "m4a",
    "mp4",
    "mov",
    "avi",
    "jpg",
    "jpeg",
    "png",
    "webp",
}


@router.post("/{project_id}/sources")
async def upload_source(
    project_id: str,
    file: UploadFile = File(...),
):

    # ---------------------------------
    # Save temporary upload
    # ---------------------------------

    temp_directory = Path("temp")

    temp_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_name = Path(
        file.filename or "uploaded_file"
    ).name

    temp_file = (
        temp_directory / file_name
    )

    content = await file.read()

    temp_file.write_bytes(
        content
    )

    # ---------------------------------
    # Determine source type
    # ---------------------------------

    source_type = (
        Path(file_name)
        .suffix
        .lower()
        .replace(".", "")
        or "unknown"
    )

    # ---------------------------------
    # Store original file
    # ---------------------------------

    source = add_source(
        project_id=project_id,
        file_path=str(temp_file),
        source_type=source_type,
        mime_type=(
            file.content_type
            or "application/octet-stream"
        ),
    )

    # ---------------------------------
    # Unsupported file
    # ---------------------------------

    if source_type not in SUPPORTED_TYPES:

        from database.repository import (
            update_knowledge_source_status,
        )

        update_knowledge_source_status(
            source.id,
            "failed",
        )

        source = update_knowledge_source_status(
            source.id,
            "failed",
        )

        return {
            "id": source.id,
            "project_id": source.project_id,
            "name": source.name,
            "source_type": source.source_type,
            "mime_type": source.mime_type,
            "file_size": source.file_size,
            "status": source.status,
            "message": (
                f"Unsupported file type: "
                f".{source_type}"
            ),
        }

    # ---------------------------------
    # Ingest immediately
    # ---------------------------------

    try:

        source = ingest_source(
            source_id=source.id,
        )

    except Exception as exc:

        # ingest_source already changes
        # status to failed.

        source = (
            __import__(
                "database.repository",
                fromlist=[
                    "get_knowledge_source"
                ],
            )
            .get_knowledge_source(
                source.id
            )
        )

        return {
            "id": source.id,
            "project_id": source.project_id,
            "name": source.name,
            "source_type": source.source_type,
            "mime_type": source.mime_type,
            "file_size": source.file_size,
            "status": source.status,
            "message": str(exc),
        }

    # ---------------------------------
    # Return final status
    # ---------------------------------

    return {
        "id": source.id,
        "project_id": source.project_id,
        "name": source.name,
        "source_type": source.source_type,
        "mime_type": source.mime_type,
        "file_size": source.file_size,
        "status": source.status,
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


@router.get("/{project_id}/sources/{source_id}/view")
def view_source(
    project_id: str,
    source_id: str,
):
    source = get_knowledge_source(source_id)

    if source is None:
        raise ValueError(
            f"Knowledge source '{source_id}' does not exist."
        )

    if source.project_id != project_id:
        raise ValueError(
            "Knowledge source does not belong to this project."
        )

    file_path = Path(source.storage_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    return FileResponse(
        path=file_path,
        media_type=source.mime_type,
        filename=source.name,
        content_disposition_type="inline",
    )


@router.get("/{project_id}/sources/{source_id}/download")
def download_source(
    project_id: str,
    source_id: str,
):
    source = get_knowledge_source(source_id)

    if source is None:
        raise ValueError(
            f"Knowledge source '{source_id}' does not exist."
        )

    if source.project_id != project_id:
        raise ValueError(
            "Knowledge source does not belong to this project."
        )

    file_path = Path(source.storage_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    return FileResponse(
        path=file_path,
        media_type=source.mime_type,
        filename=source.name,
        content_disposition_type="attachment",
    )