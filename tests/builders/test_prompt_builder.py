from pathlib import Path

from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.scanner.scanner import Scanner


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