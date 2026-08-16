from pathlib import Path


class GitRepository:

    @staticmethod
    def discover(path: Path) -> Path:
        current = path.resolve()

        while True:
            if (current / ".git").is_dir():
                return current

            if current.parent == current:
                return path.resolve()

            current = current.parent