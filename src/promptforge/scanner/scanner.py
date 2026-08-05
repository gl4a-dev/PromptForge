from pathlib import Path

from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory
from promptforge.models.scan_result import ScanResult


class Scanner:

    def scan(self, root: Path) -> ScanResult:
        directories: list[ProjectDirectory] = []
        files: list[ProjectFile] = []

        for path in root.rglob("*"):
            if path.is_dir():
                directories.append(ProjectDirectory(path))

            elif path.is_file():
                files.append(ProjectFile(path))

        return ScanResult(
            directories=directories,
            files=files,
        )