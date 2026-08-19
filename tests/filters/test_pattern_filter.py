from pathlib import Path

from promptforge.models.project_file import ProjectFile
from promptforge.filters.pattern_filter import PatternFilter


def create_filter(
    scan_root: Path,
    patterns: list[str],
) -> PatternFilter:

    return PatternFilter(
        scan_root=scan_root,
        patterns=patterns,
    )


def test_load_patterns(tmp_path: Path) -> None:
    patterns = [".venv/", "__pycache__/", "*.pyc", "dist/"]

    filter_ = create_filter(tmp_path, patterns)

    assert filter_._patterns == [
        ".venv/",
        "__pycache__/",
        "*.pyc",
        "dist/",
    ]

def test_load_patterns_without_patterns(tmp_path: Path) -> None:
    filter_ = create_filter(tmp_path, [])

    assert filter_._patterns == []

def test_ignore_directory(tmp_path: Path) -> None:
    file = tmp_path / ".venv" / "config.py"
    file.parent.mkdir()
    file.touch()

    filter_ = create_filter(tmp_path, [".venv/"])

    assert not filter_.accept_file(ProjectFile(file))

def test_keep_regular_file(tmp_path: Path) -> None:
    file = tmp_path / "src" / "main.py"
    file.parent.mkdir()
    file.touch()

    filter_ = create_filter(tmp_path, [".venv/"])

    assert filter_.accept_file(ProjectFile(file))

def test_ignore_pycache(tmp_path: Path) -> None:
    file = tmp_path / "src" / "__pycache__" / "main.cpython-312.pyc"
    file.parent.mkdir(parents=True)
    file.touch()

    filter_ = create_filter(tmp_path, ["__pycache__/"])

    assert not filter_.accept_file(ProjectFile(file))

def test_ignore_extension(tmp_path: Path) -> None:
    file = tmp_path / "src" / "module.pyc"
    file.parent.mkdir()
    file.touch()

    filter_ = create_filter(tmp_path, ["*.pyc"])

    assert not filter_.accept_file(ProjectFile(file))

def test_without_pattern_accept_everything(tmp_path: Path) -> None:
    file = tmp_path / "main.py"
    file.touch()

    filter_ = create_filter(tmp_path, [])

    assert filter_.accept_file(ProjectFile(file))

def test_negated_pattern_keeps_file(tmp_path: Path) -> None:
    main = tmp_path / "main.py"
    main.touch()

    filter_ = create_filter(tmp_path, ["*.py", "!main.py"])

    assert filter_.accept_file(ProjectFile(main))

def test_negated_pattern_only_affects_matching_file(tmp_path: Path) -> None:
    utils = tmp_path / "utils.py"
    utils.touch()

    filter_ = create_filter(tmp_path, ["*.py", "!main.py"])

    assert not filter_.accept_file(ProjectFile(utils))

def test_negated_pattern_inside_directory(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()

    readme = docs / "README.md"
    readme.touch()

    filter_ = create_filter(tmp_path, ["docs/*", "!docs/README.md"])

    assert filter_.accept_file(ProjectFile(readme))

def test_negated_pattern_does_not_keep_other_files(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()

    guide = docs / "guide.md"
    guide.touch()

    filter_ = create_filter(tmp_path, ["docs/*", "!docs/README.md"])

    assert not filter_.accept_file(ProjectFile(guide))

def test_accept_file_with_symlink_inside_repository(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        ".venv/\n",
        encoding="utf-8",
    )

    venv = tmp_path / ".venv"
    venv.mkdir()

    python = venv / "python"

    target = Path("/usr/bin/python3")
    if target.exists():
        python.symlink_to(target)

        filter_ = create_filter(tmp_path, [".venv/"])

        assert not filter_.accept_file(ProjectFile(python))