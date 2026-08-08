from promptforge.models.project_file import ProjectFile


class FileReader:

    def read(self, file: ProjectFile) -> str:
        return file.path.read_text(encoding="utf-8")