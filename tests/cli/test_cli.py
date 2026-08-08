from pathlib import Path

from click.testing import CliRunner

from promptforge.cli.main import main


def test_main_generates_prompt_with_gitignore(
    tmp_path: Path,
) -> None:
    main_file = tmp_path / "main.py"
    main_file.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    ignored_file = tmp_path / "secret.py"
    ignored_file.write_text(
        "this should not appear\n",
        encoding="utf-8",
    )

    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(
        "secret.py\n",
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(tmp_path)],
    )

    assert result.exit_code == 0

    assert "main.py" in result.output
    assert 'print("Hello")' in result.output

    assert "## secret.py" not in result.output
    assert "this should not appear" not in result.output