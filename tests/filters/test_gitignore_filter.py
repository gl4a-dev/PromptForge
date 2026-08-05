from pathlib import Path

from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory
from promptforge.filters.gitignore_filter import GitIgnoreFilter


def test_load_patterns(tmp_path: Path) -> None:
    gitignore = tmp_path / ".gitignore"

    gitignore.write_text(
        """
        # Comment

        .venv/
        __pycache__/

        *.pyc

        dist/
        """
    )

    filter_ = GitIgnoreFilter(tmp_path)

    assert filter_._patterns == [
        ".venv/",
        "__pycache__/",
        "*.pyc",
        "dist/",
    ]

def test_load_patterns_without_gitignore(tmp_path: Path) -> None:
    filter_ = GitIgnoreFilter(tmp_path)

    assert filter_._patterns == []

def test_ignore_directory(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(".venv/\n")

    file = tmp_path / ".venv" / "config.py"
    file.parent.mkdir()
    file.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert not filter_.accept_file(ProjectFile(file))

def test_keep_regular_file(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(".venv/\n")

    file = tmp_path / "src" / "main.py"
    file.parent.mkdir()
    file.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert filter_.accept_file(ProjectFile(file))

def test_ignore_pycache(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text("__pycache__/\n")

    file = tmp_path / "src" / "__pycache__" / "main.cpython-312.pyc"
    file.parent.mkdir(parents=True)
    file.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert not filter_.accept_file(ProjectFile(file))

def test_ignore_extension(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text("*.pyc\n")

    file = tmp_path / "src" / "module.pyc"
    file.parent.mkdir()
    file.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert not filter_.accept_file(ProjectFile(file))

def test_without_gitignore_accept_everything(tmp_path: Path) -> None:
    file = tmp_path / "main.py"
    file.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert filter_.accept_file(ProjectFile(file))

def test_ignore_comments_and_blank_lines(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        """
        # Comment

        .venv/

        """
    )

    file = tmp_path / ".venv" / "file.py"
    file.parent.mkdir()
    file.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert not filter_.accept_file(ProjectFile(file))

def test_negated_pattern_keeps_file(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        """
        *.py
        !main.py
        """
    )

    main = tmp_path / "main.py"
    main.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert filter_.accept_file(ProjectFile(main))

def test_negated_pattern_only_affects_matching_file(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        """
        *.py
        !main.py
        """
    )

    utils = tmp_path / "utils.py"
    utils.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert not filter_.accept_file(ProjectFile(utils))

def test_negated_pattern_inside_directory(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        """
        docs/*
        !docs/README.md
        """
    )

    docs = tmp_path / "docs"
    docs.mkdir()

    readme = docs / "README.md"
    readme.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert filter_.accept_file(ProjectFile(readme))

def test_negated_pattern_does_not_keep_other_files(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        """
        docs/*
        !docs/README.md
        """
    )

    docs = tmp_path / "docs"
    docs.mkdir()

    guide = docs / "guide.md"
    guide.touch()

    filter_ = GitIgnoreFilter(tmp_path)

    assert not filter_.accept_file(ProjectFile(guide))