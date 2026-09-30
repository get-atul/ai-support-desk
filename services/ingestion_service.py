from pathlib import Path

from core.document import DocumentContent
from core.vector_store import add_document
from database.repository import (
    get_knowledge_source,
    update_knowledge_source_status,
)


def ingest_text_source(
    source_id: str,
) -> DocumentContent:

    source = get_knowledge_source(source_id)

    if source is None:
        raise ValueError(
            f"Knowledge source '{source_id}' does not exist."
        )

    update_knowledge_source_status(
        source_id,
        "processing",
    )

    try:

        file_path = Path(source.storage_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Source file not found: {file_path}"
            )

        text = file_path.read_text(
            encoding="utf-8"
        )

        document = DocumentContent(
            text=text,
            source_id=source.id,
            project_id=source.project_id,
            source_name=source.name,
            source_type=source.source_type,
            language="en",
        )

        add_document(document)

        update_knowledge_source_status(
            source_id,
            "completed",
        )

        return document

    except Exception:

        update_knowledge_source_status(
            source_id,
            "failed",
        )

        raise


def index_document(
    document: DocumentContent,
):
    print("Starting vector indexing...")

    result = add_document(document)

    print("Vector indexing completed.")

    return result