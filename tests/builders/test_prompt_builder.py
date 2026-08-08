from pathlib import Path

from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.scanner.scanner import Scanner
from promptforge.filters.gitignore_filter import GitIgnoreFilter
from promptforge.filters.pipline import FilterPipeline


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
        tmp_path.name,
        "├── src",
        "│   └── main.py",
        "└── README.md",
        "",
        "# File Contents",
        "",
        "## src/main.py",
        "",
        "```python",
        'print("Hello")',
        "```",
        "",
        "## README.md",
        "",
        "```markdown",
        "# Example",
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
        GitIgnoreFilter(tmp_path),
    ])

    filtered = pipeline.apply(scan_result)

    result = PromptBuilder().build(filtered)

    assert "src/main.py" in result
    assert 'print("Hello")' in result

    assert "## cache.py" not in result
    assert "should not appear" not in result