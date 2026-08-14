from pathlib import Path
import pytest

from promptforge.formatters.content_formatter import ContentFormatter
from promptforge.readers.file_reader import FileReader
from promptforge.scanner.scanner import Scanner


def test_format_relative_path(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    file_path = src / "main.py"
    file_path.write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    scan_result = Scanner().scan(tmp_path)
    file = scan_result.files[0]

    content = FileReader().read(file)

    result = ContentFormatter().format(
        file,
        content,
        scan_result,
    )

    assert result == (
        "## src/main.py\n\n"
        "```python\n"
        "print('hello')\n"
        "\n```\n"
    )

def test_format_does_not_include_absolute_path(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    file_path = src / "main.py"
    file_path.write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    scan_result = Scanner().scan(tmp_path)
    file = scan_result.files[0]

    content = FileReader().read(file)

    result = ContentFormatter().format(
        file,
        content,
        scan_result,
    )

    assert "src/main.py" in result
    assert str(tmp_path) not in result

@pytest.mark.parametrize(
    ("filename", "content", "language"),
    [
        ("main.py", "print('hello')\n", "python"),
        ("script.js", "console.log('hello');\n", "javascript"),
        ("README.md", "# Hello\n", "markdown"),
    ],
)
def test_format_known_language(tmp_path: Path, filename: str, content: str, language: str) -> None:
    file_path = tmp_path / filename
    file_path.write_text(content, encoding="utf-8")

    scan_result = Scanner().scan(tmp_path)
    file = scan_result.files[0]

    content = FileReader().read(file)

    result = ContentFormatter().format(
        file,
        content,
        scan_result,
    )

    assert result == (
        f"## {filename}\n\n"
        f"```{language}\n"
        f"{content}"
        "\n```\n"
    )