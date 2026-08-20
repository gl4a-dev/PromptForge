from pathlib import Path
import pytest

from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.scanner.scanner import Scanner
from promptforge.filters.gitignore_filter import GitIgnoreFilter
from promptforge.filters.pipline import FilterPipeline


@pytest.mark.parametrize(
    "build_tree, build_content",
    [
        (True, True),
        (True, False),
        (False, True),
    ],
)
def test_build_prompt_valid_initialization(build_tree: bool, build_content: bool) -> None:
    PromptBuilder(
        build_tree=build_tree,
        build_content=build_content,
    )

def test_build_prompt_invalid_initialization() -> None:
    with pytest.raises(ValueError):
        PromptBuilder(
            build_tree=False,
            build_content=False,
        )

def test_build_prompt(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    main = src / "main.py"
    main.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Example\n",
        encoding="utf-8",
    )

    scan_result = Scanner().scan(tmp_path)

    result = PromptBuilder().build(scan_result)

    assert result == "\n".join([
        "# Project Structure",
        "",
        "```text",
        tmp_path.name,
        "├── src",
        "│   └── main.py",
        "└── README.md",
        "```",
        "",
        "# File Contents",
        "",
        "## src/main.py",
        "",
        "```python",
        'print("Hello")',
        "",
        "```",
        "",
        "## README.md",
        "",
        "```markdown",
        "# Example",
        "",
        "```",
        "",
    ])

def test_build_only_tree_prompt(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    main = src / "main.py"
    main.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Example\n",
        encoding="utf-8",
    )

    scan_result = Scanner().scan(tmp_path)

    result = PromptBuilder(
        build_tree=True, 
        build_content=False
    ).build(scan_result)

    assert result == "\n".join([
        "# Project Structure",
        "",
        "```text",
        tmp_path.name,
        "├── src",
        "│   └── main.py",
        "└── README.md",
        "```",
    ])

def test_build_only_content_prompt(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    main = src / "main.py"
    main.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Example\n",
        encoding="utf-8",
    )

    scan_result = Scanner().scan(tmp_path)

    result = PromptBuilder(
        build_tree=False, 
        build_content=True
    ).build(scan_result)

    assert result == "\n".join([
        "# File Contents",
        "",
        "## src/main.py",
        "",
        "```python",
        'print("Hello")',
        "",
        "```",
        "",
        "## README.md",
        "",
        "```markdown",
        "# Example",
        "",
        "```",
        "",
    ])

def test_build_prompt_with_filter(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    main = src / "main.py"
    main.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    cache = tmp_path / "cache.py"
    cache.write_text(
        "should not appear\n",
        encoding="utf-8",
    )

    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(
        "cache.py\n",
        encoding="utf-8",
    )

    scan_result = Scanner().scan(tmp_path)

    pipeline = FilterPipeline([
        GitIgnoreFilter(tmp_path, tmp_path),
    ])

    filtered = pipeline.apply(scan_result)

    result = PromptBuilder().build(filtered)

    assert "src/main.py" in result
    assert 'print("Hello")' in result

    assert "## cache.py" not in result
    assert "should not appear" not in result

def test_build_prompt_ignores_binary_files(tmp_path: Path) -> None:
    main = tmp_path / "main.py"
    main.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    image = tmp_path / "image.png"
    image.write_bytes(
        b"\x89PNG\r\n\x1a\n"
    )

    scan_result = Scanner().scan(tmp_path)

    result = PromptBuilder().build(scan_result)

    assert "main.py" in result
    assert 'print("Hello")' in result

    assert "image.png" in result
    assert "## image.png" not in result