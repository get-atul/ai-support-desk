from pathlib import Path
import shutil


STORAGE_ROOT = Path("storage")


class LocalFileStorage:

    def __init__(self, root: Path = STORAGE_ROOT):
        self.root = root

    def save(
        self,
        project_id: str,
        source_id: str,
        file_path: str,
    ) -> str:

        source_directory = (
            self.root
            / "projects"
            / project_id
            / "sources"
            / source_id
        )

        source_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        original_file = Path(file_path)

        destination = (
            source_directory
            / original_file.name
        )

        shutil.copy2(
            original_file,
            destination,
        )

        return str(destination)

    def get(
        self,
        project_id: str,
        source_id: str,
        file_name: str,
    ) -> Path:

        file_path = (
            self.root
            / "projects"
            / project_id
            / "sources"
            / source_id
            / file_name
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        return file_path