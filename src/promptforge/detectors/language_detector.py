from pathlib import Path

from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

from promptforge.models.project_file import ProjectFile


class LanguageDetector:

    def detect(self, file: ProjectFile) -> str | None:
        try:
            lexer = get_lexer_for_filename(file.path.name)
        except ClassNotFound:
            return None

        return lexer.name