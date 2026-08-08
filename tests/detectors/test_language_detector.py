from pathlib import Path
import pytest

from promptforge.detectors.language_detector import LanguageDetector
from promptforge.models.project_file import ProjectFile


@pytest.mark.parametrize(
    ("filename", "expected_language"),
    [
        ("main.py", "Python"),
        ("script.js", "JavaScript"),
        ("README.md", "Markdown"),
    ],
)
def test_detect_known_language(tmp_path: Path, filename: str, expected_language: str) -> None:
    file = ProjectFile(tmp_path / filename)

    result = LanguageDetector().detect(file)

    assert result == expected_language


def test_unknown_extension(tmp_path: Path) -> None:
    file = ProjectFile(tmp_path / "file.xyz")

    result = LanguageDetector().detect(file)

    assert result is None