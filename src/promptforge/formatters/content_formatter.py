from promptforge.detectors.language_detector import LanguageDetector
from promptforge.models.project_file import ProjectFile
from promptforge.models.scan_result import ScanResult


class ContentFormatter:

    def __init__(self) -> None:
        self._language_detector = LanguageDetector()

    def format(self, file: ProjectFile, content: str, scan_result: ScanResult) -> str:
        relative_path = file.path.relative_to(
            scan_result.root.path
        )

        language = self._language_detector.detect(file)
        language_identifier = self._get_language_identifier(language)

        return (
            f"## {relative_path}\n\n"
            f"```{language_identifier}\n"
            f"{content}"
            f"\n```\n"
        )

    def _get_language_identifier(self, language: str | None) -> str:
        if language is None:
            return ""

        return language.lower()