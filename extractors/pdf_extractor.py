from pathlib import Path

from pypdf import PdfReader

from core.document import DocumentContent
from extractors.ocr_extractor import extract_pdf_ocr


def extract_pdf(
    file_path: str,
    source_id: str,
    project_id: str,
    source_name: str,
) -> DocumentContent:

    reader = PdfReader(
        Path(file_path)
    )

    pages = []

    extracted_character_count = 0

    # ---------------------------------
    # 1. Try normal PDF text extraction
    # ---------------------------------

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):

        text = page.extract_text() or ""

        text = text.strip()

        if text:

            extracted_character_count += len(text)

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    # ---------------------------------
    # 2. OCR fallback for scanned PDFs
    # ---------------------------------

    if extracted_character_count < 50:

        print(
            "Little/no text found in PDF. "
            "Starting OCR fallback..."
        )

        pages = extract_pdf_ocr(
            file_path
        )

    # ---------------------------------
    # 3. Build final document
    # ---------------------------------

    formatted_pages = []

    for page in pages:

        formatted_pages.append(
            f"[Page {page['page_number']}]\n"
            f"{page['text']}"
        )

    return DocumentContent(
        text="\n\n".join(
            formatted_pages
        ),
        source_id=source_id,
        project_id=project_id,
        source_name=source_name,
        source_type="pdf",
        language="en",
        metadata={
            "page_count": len(reader.pages),
            "ocr_used": (
                extracted_character_count < 50
            ),
        },
    )