from promptforge.filters.filter import Filter
from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


class AcceptAllFilter(Filter):

    def accept_file(self, file: ProjectFile) -> bool:
        return True

    def accept_directory(self, directory: ProjectDirectory) -> bool:
        return True