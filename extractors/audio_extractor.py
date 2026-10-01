import os

from openai import OpenAI

from core.document import DocumentContent


def extract_audio(
    file_path: str,
    source_id: str,
    project_id: str,
    source_name: str,
) -> DocumentContent:

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    with open(file_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )

    return DocumentContent(
        text=transcription.text,
        source_id=source_id,
        project_id=project_id,
        source_name=source_name,
        source_type="audio",
        language="en",
    )