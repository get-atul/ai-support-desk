from pathlib import Path
from uuid import uuid4

from core.storage import LocalFileStorage
from database.repository import create_knowledge_source


storage = LocalFileStorage()


def add_source(
    project_id: str,
    file_path: str,
    source_type: str,
    mime_type: str,
):
    source_id = str(uuid4())

    original_file = Path(file_path)

    stored_path = storage.save(
        project_id=project_id,
        source_id=source_id,
        file_path=file_path,
    )

    file_size = original_file.stat().st_size

    source = create_knowledge_source(
        source_id=source_id,
        project_id=project_id,
        name=original_file.name,
        source_type=source_type,
        storage_path=stored_path,
        mime_type=mime_type,
        file_size=file_size,
    )

    return source