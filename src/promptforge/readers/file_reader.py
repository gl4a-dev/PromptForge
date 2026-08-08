from promptforge.models.project_file import ProjectFile


class FileReader:

    def read(self, file: ProjectFile) -> str | None:
        try:
            return file.path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None