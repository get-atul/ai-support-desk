import base64
import os

from openai import OpenAI

from core.document import DocumentContent


def extract_image(
    file_path: str,
    source_id: str,
    project_id: str,
    source_name: str,
) -> DocumentContent:

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    with open(file_path, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
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
                            "Extract all useful text from "
                            "this image. If the image contains "
                            "diagrams, tables, screenshots, "
                            "or other useful information, "
                            "describe that information too."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            f"data:image/jpeg;base64,"
                            f"{encoded_image}"
                        ),
                    },
                ],
            }
        ],
    )

    return DocumentContent(
        text=response.output_text,
        source_id=source_id,
        project_id=project_id,
        source_name=source_name,
        source_type="image",
        language="en",
    )