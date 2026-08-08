from pathlib import Path

from promptforge.models.project_file import ProjectFile
from promptforge.readers.file_reader import FileReader


def test_read_file(tmp_path: Path) -> None:
    path = tmp_path / "example.py"
    path.write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    file = ProjectFile(path)

    result = FileReader().read(file)

    assert result == "print('hello')\n"

def test_read_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.txt"
    path.write_text("", encoding="utf-8")

    file = ProjectFile(path)

    result = FileReader().read(file)

    assert result == ""

def test_read_utf8_file(tmp_path: Path) -> None:
    path = tmp_path / "example.txt"
    path.write_text(
        "Olá, mundo! 🌎\n",
        encoding="utf-8",
    )

    file = ProjectFile(path)

    result = FileReader().read(file)

    assert result == "Olá, mundo! 🌎\n"

def test_read_preserves_content(tmp_path: Path) -> None:
    content = (
        "def hello():\n"
        "    print('Hello')\n"
        "\n"
        "hello()\n"
    )

    path = tmp_path / "example.py"
    path.write_text(content, encoding="utf-8")

    file = ProjectFile(path)

    result = FileReader().read(file)

    assert result == content

def test_read_binary_file_returns_none(tmp_path: Path) -> None:
    file_path = tmp_path / "image.png"

    file_path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
    )

    project_file = ProjectFile(file_path)

    result = FileReader().read(project_file)

    assert result is None