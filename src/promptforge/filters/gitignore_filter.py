from pathlib import Path
from pathspec import PathSpec

from promptforge.filters.filter import Filter
from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


class GitIgnoreFilter(Filter):

    def __init__(
        self,
        scan_root: Path,
        git_root: Path,
    ) -> None:
        self._scan_root = scan_root.resolve()
        self._git_root = git_root.resolve()

        self._gitignore = self._git_root / ".gitignore"

        self._patterns = self._load_patterns()
        self._spec = PathSpec.from_lines("gitignore", self._patterns)

    def _load_patterns(self) -> list[str]:
        if not self._gitignore.exists():
            return []

        patterns: list[str] = []

        for line in self._gitignore.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            patterns.append(line)

        return patterns

    def _accept_path(self, path: Path) -> bool:
        relative_path = path.relative_to(self._git_root)

        if relative_path.parts and relative_path.parts[0] == ".git":
            return False

        path_string = relative_path.as_posix()

        if path.is_dir():
            path_string += "/"

        return not self._spec.match_file(path_string)

    def accept_file(self, file: ProjectFile) -> bool:
        return self._accept_path(file.path)

    def accept_directory(self, directory: ProjectDirectory) -> bool:
        return self._accept_path(directory.path)