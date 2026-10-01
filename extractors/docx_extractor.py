from docx import Document

from core.document import DocumentContent


def extract_docx(
    file_path: str,
    source_id: str,
    project_id: str,
    source_name: str,
) -> DocumentContent:

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return DocumentContent(
        text="\n\n".join(paragraphs),
        source_id=source_id,
        project_id=project_id,
        source_name=source_name,
        source_type="docx",
        language="en",
    )