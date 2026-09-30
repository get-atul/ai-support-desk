from core.vector_store import add_document
from pathlib import Path

from core.document import DocumentContent


def ingest_text_source(
    source_id: str,
    project_id: str,
    source_name: str,
    storage_path: str,
    source_type: str,
) -> DocumentContent:

    file_path = Path(storage_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    text = file_path.read_text(
        encoding="utf-8"
    )

    return DocumentContent(
        text=text,
        source_id=source_id,
        project_id=project_id,
        source_name=source_name,
        source_type=source_type,
        language="en",
    )

def index_document(
    document: DocumentContent,
):
    return add_document(document)