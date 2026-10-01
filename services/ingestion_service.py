from pathlib import Path

from core.vector_store import add_document

from database.repository import (
    get_knowledge_source,
    update_knowledge_source_status,
)

from extractors.text_extractor import extract_text
from extractors.pdf_extractor import extract_pdf
from extractors.docx_extractor import extract_docx
from extractors.audio_extractor import extract_audio
from extractors.video_extractor import extract_video
from extractors.image_extractor import extract_image


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


def ingest_source(
    source_id: str,
):

    source = get_knowledge_source(
        source_id
    )

    if source is None:
        raise ValueError(
            f"Knowledge source '{source_id}' does not exist."
        )

    # ---------------------------------
    # Mark source as processing
    # ---------------------------------

    update_knowledge_source_status(
        source_id,
        "processing",
    )

    try:

        file_path = Path(
            source.storage_path
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"Source file not found: {file_path}"
            )

        source_type = (
            source.source_type
            .lower()
            .strip()
        )

        # ---------------------------------
        # Validate source type
        # ---------------------------------

        if source_type not in SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported source type: {source_type}"
            )

        common_args = {
            "file_path": str(file_path),
            "source_id": source.id,
            "project_id": source.project_id,
            "source_name": source.name,
        }

        # ---------------------------------
        # Extract content
        # ---------------------------------

        if source_type == "txt":

            document = extract_text(
                **common_args
            )

        elif source_type == "pdf":

            document = extract_pdf(
                **common_args
            )

        elif source_type == "docx":

            document = extract_docx(
                **common_args
            )

        elif source_type in {
            "mp3",
            "wav",
            "m4a",
        }:

            document = extract_audio(
                **common_args
            )

        elif source_type in {
            "mp4",
            "mov",
            "avi",
        }:

            document = extract_video(
                **common_args
            )

        elif source_type in {
            "jpg",
            "jpeg",
            "png",
            "webp",
        }:

            document = extract_image(
                **common_args
            )

        else:

            raise ValueError(
                f"No extractor configured for: "
                f"{source_type}"
            )

        # ---------------------------------
        # Validate extracted content
        # ---------------------------------

        if not document.text.strip():

            raise ValueError(
                "No text could be extracted "
                "from the source."
            )

        # ---------------------------------
        # Add to vector database
        # ---------------------------------

        add_document(
            document
        )

        # ---------------------------------
        # Mark ingestion as completed
        # ---------------------------------

        update_knowledge_source_status(
            source_id,
            "completed",
        )

        print(
            f"Ingestion completed: "
            f"{source.name}"
        )

        return get_knowledge_source(
            source_id
        )

    except Exception as exc:

        print(
            f"Ingestion failed for "
            f"{source.name}: {exc}"
        )

        # ---------------------------------
        # IMPORTANT:
        # Never leave the source in
        # "processing" or "pending"
        # after an ingestion error.
        # ---------------------------------

        update_knowledge_source_status(
            source_id,
            "failed",
        )

        raise


def ingest_text_source(
    source_id: str,
):

    return ingest_source(
        source_id
    )