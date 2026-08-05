from pathlib import Path

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