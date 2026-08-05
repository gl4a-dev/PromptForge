from abc import ABC, abstractmethod

from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory


class Filter(ABC):

    @abstractmethod
    def accept_file(self, file: ProjectFile) -> bool:
        """Returns True if the file should be kept."""
        ...

    @abstractmethod
    def accept_directory(self, directory: ProjectDirectory) -> bool:
        """Returns True if the directory should be kept."""
        ...