import os
import subprocess
import tempfile

from openai import OpenAI

from core.document import DocumentContent


def extract_video(
    file_path: str,
    source_id: str,
    project_id: str,
    source_name: str,
) -> DocumentContent:

    print(
        f"Processing video: {file_path}"
    )

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Video file does not exist: {file_path}"
        )

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    audio_path = None

    try:

        # ---------------------------------
        # Extract audio from video
        # ---------------------------------

        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False,
        ) as temp_audio:

            audio_path = temp_audio.name

        print(
            "Extracting audio from video..."
        )

        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                file_path,
                "-vn",
                "-acodec",
                "mp3",
                audio_path,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            raise RuntimeError(
                "FFmpeg failed to extract audio.\n\n"
                f"FFmpeg error:\n{result.stderr}"
            )

        if not os.path.exists(audio_path):

            raise RuntimeError(
                "FFmpeg completed but did not "
                "create the audio file."
            )

        print(
            f"Audio extracted: {audio_path}"
        )

        # ---------------------------------
        # Transcribe audio
        # ---------------------------------

        print(
            "Transcribing video audio..."
        )

        with open(
            audio_path,
            "rb",
        ) as audio_file:

            transcription = (
                client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio_file,
                )
            )

        text = transcription.text.strip()

        if not text:

            raise ValueError(
                "No speech could be detected "
                "in the video."
            )

        print(
            "Video transcription completed."
        )

        return DocumentContent(
            text=text,
            source_id=source_id,
            project_id=project_id,
            source_name=source_name,
            source_type="video",
            language="en",
        )

    finally:

        # ---------------------------------
        # Delete temporary audio
        # ---------------------------------

        if (
            audio_path
            and os.path.exists(audio_path)
        ):

            os.remove(
                audio_path
            )