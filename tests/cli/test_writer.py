from pathlib import Path

from promptforge.cli.writer import PromptWriter

def test_write_output_file(tmp_path: Path):
    output = tmp_path / "prompt.md"

    PromptWriter.write(
        "├── main.py",
        output,
    )

    assert output.read_text(
        encoding="utf-8"
    ) == "├── main.py"

def test_write_prompt_to_file(tmp_path: Path) -> None:
    output = tmp_path / "prompt.md"

    PromptWriter.write(
        prompt="├── main.py",
        output=output,
    )

    assert output.exists()

    assert output.read_text(
        encoding="utf-8",
    ) == "├── main.py"