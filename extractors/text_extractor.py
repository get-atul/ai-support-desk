from pathlib import Path

from core.document import DocumentContent


def extract_text(
    file_path: str,
    source_id: str,
    project_id: str,
    source_name: str,
) -> DocumentContent:

    text = Path(file_path).read_text(
        encoding="utf-8"
    )

    return DocumentContent(
        text=text,
        source_id=source_id,
        project_id=project_id,
        source_name=source_name,
        source_type="txt",
        language="en",
    )