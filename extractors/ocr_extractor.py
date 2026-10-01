import base64
import os

import pymupdf
from openai import OpenAI


def extract_pdf_ocr(
    file_path: str,
) -> list[dict]:

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    pdf = pymupdf.open(file_path)

    pages = []

    try:
        for page_number, page in enumerate(
            pdf,
            start=1,
        ):
            print(
                f"OCR processing PDF page {page_number}..."
            )

            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False,
            )

            image_bytes = pixmap.tobytes(
                "png"
            )

            encoded_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            response = client.responses.create(
                model="gpt-5-nano",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Extract all useful information "
                                    "from this document page. "
                                    "Preserve the actual text as "
                                    "accurately as possible. "
                                    "Also describe important tables, "
                                    "forms, diagrams, or other "
                                    "information that would be useful "
                                    "for searching this document. "
                                    "Do not add information that is "
                                    "not present on the page."
                                ),
                            },
                            {
                                "type": "input_image",
                                "image_url": (
                                    "data:image/png;base64,"
                                    f"{encoded_image}"
                                ),
                            },
                        ],
                    }
                ],
            )

            text = response.output_text.strip()

            if text:
                pages.append(
                    {
                        "page_number": page_number,
                        "text": text,
                    }
                )

    finally:
        pdf.close()

    return pages