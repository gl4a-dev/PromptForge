from pathlib import Path
from pathspec import PathSpec

from promptforge.filters.filter import Filter
from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


class PatternFilter(Filter):

    def __init__(
        self,
        scan_root: Path,
        patterns: list[str]
    ) -> None:
        self._scan_root = scan_root
        self._patterns = patterns
        self._spec = PathSpec.from_lines("gitignore", self._patterns)

    def _accept_path(self, path: Path) -> bool:
        relative_path = path.relative_to(self._scan_root)

        path_string = relative_path.as_posix()

        if path.is_dir():
            path_string += "/"

        return not self._spec.match_file(path_string)

    def accept_file(self, file: ProjectFile) -> bool:
        return self._accept_path(file.path)

    def accept_directory(self, directory: ProjectDirectory) -> bool:
        return self._accept_path(directory.path)