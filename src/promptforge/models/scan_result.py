from dataclasses import dataclass

from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


@dataclass(slots=True)
class ScanResult:
    root: ProjectDirectory
    directories: list[ProjectDirectory]
    files: list[ProjectFile]