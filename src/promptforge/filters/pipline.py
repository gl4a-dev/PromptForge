from promptforge.filters.filter import Filter
from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory
from promptforge.models.scan_result import ScanResult


class FilterPipeline:

    def __init__(self, filters: list[Filter]) -> None:
        self._filters = filters

    def _accept_directory(self, directory: ProjectDirectory) -> bool:
        return all(
            filter_.accept_directory(directory)
            for filter_ in self._filters
        )
    
    def _accept_file(self, file: ProjectFile) -> bool:
        return all(
            filter_.accept_file(file)
            for filter_ in self._filters
        )

    def _filter_directories(self, directories: list[ProjectDirectory]) -> list[ProjectDirectory]:
        return [
            directory for directory in directories
            if self._accept_directory(directory)
        ]

    def _filter_files(self, files: list[ProjectFile]) -> list[ProjectFile]:
        return [
            file for file in files
            if self._accept_file(file)
        ]

    def apply(self, scan_result: ScanResult) -> ScanResult:
        return ScanResult(
            root=scan_result.root,
            directories=self._filter_directories(scan_result.directories),
            files=self._filter_files(scan_result.files),
        )