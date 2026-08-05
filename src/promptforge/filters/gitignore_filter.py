from pathlib import Path


class GitIgnoreFilter:

    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root
        self._gitignore = project_root / ".gitignore"

        self._patterns = self._load_patterns()

    def _load_patterns(self) -> list[str]:
        if not self._gitignore.exists():
            return []

        patterns: list[str] = []

        for line in self._gitignore.read_text().splitlines():
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            patterns.append(line)

        return patterns