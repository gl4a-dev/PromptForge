from pathlib import Path

from promptforge.filters.filter import Filter
from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


class PathFilter(Filter):

    def __init__(self, ignored_parts: set[str]) -> None:
        self._ignored_parts = ignored_parts

    def _accept_path(self, path: Path) -> bool:
        return not any(
            part in self._ignored_parts
            for part in path.parts
        )

    def accept_file(self, file: ProjectFile) -> bool:
        return self._accept_path(file.path)

    def accept_directory(self, directory: ProjectDirectory) -> bool:
        return self._accept_path(directory.path)