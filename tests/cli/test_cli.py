import pytest
from pathlib import Path
from click.testing import CliRunner

from promptforge.cli.main import (
    main, 
    _build_filter_pipeline,
    _build_prompt_forge,
)
from promptforge.cli.config import PromptForgeConfig
from promptforge.filters.pattern_filter import PatternFilter


def test_main_generates_prompt_with_gitignore(tmp_path: Path) -> None:
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

def test_main_help() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Generate a prompt from a project." in result.output
    assert "PATH" in result.output


def test_main_default_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    main_file = tmp_path / "main.py"
    main_file.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    runner = CliRunner()

    result = runner.invoke(main)

    assert result.exit_code == 0
    assert "main.py" in result.output
    assert 'print("Hello")' in result.output


def test_main_rejects_nonexistent_path(tmp_path: Path) -> None:
    nonexistent = tmp_path / "does_not_exist"

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(nonexistent)],
    )

    assert result.exit_code != 0


def test_main_rejects_file_path(tmp_path: Path) -> None:
    file = tmp_path / "main.py"
    file.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(file)],
    )

    assert result.exit_code != 0


def test_main_generates_nested_project(tmp_path: Path) -> None:
    src = tmp_path / "src"
    utils = src / "utils"

    utils.mkdir(parents=True)

    main_file = src / "main.py"
    helper_file = utils / "helper.py"

    main_file.write_text(
        "from utils.helper import hello\n",
        encoding="utf-8",
    )

    helper_file.write_text(
        'def hello():\n    return "Hello"\n',
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(tmp_path)],
    )

    assert result.exit_code == 0

    assert "src" in result.output
    assert "utils" in result.output
    assert "main.py" in result.output
    assert "helper.py" in result.output

    assert "from utils.helper import hello" in result.output
    assert 'return "Hello"' in result.output


def test_main_ignores_gitignore_directory(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    main_file = src / "main.py"
    main_file.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    cache = tmp_path / "__pycache__"
    cache.mkdir()

    cached_file = cache / "something.pyc"
    cached_file.write_bytes(b"\x00\x01\x02")

    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(
        "__pycache__/\n",
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(tmp_path)],
    )

    assert result.exit_code == 0

    assert "src" in result.output
    assert "main.py" in result.output

    assert "├── __pycache__" not in result.output
    assert "└── __pycache__" not in result.output
    assert "something.pyc" not in result.output


def test_main_ignores_git_directory(tmp_path: Path) -> None:
    git = tmp_path / ".git"
    objects = git / "objects"

    objects.mkdir(parents=True)

    git_file = objects / "some_file"
    git_file.write_text(
        "internal git data",
        encoding="utf-8",
    )

    main_file = tmp_path / "main.py"
    main_file.write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(tmp_path)],
    )

    assert result.exit_code == 0

    assert "main.py" in result.output
    assert ".git" not in result.output
    assert "some_file" not in result.output
    assert "internal git data" not in result.output

def test_cli_output_option(tmp_path: Path) -> None:
    runner = CliRunner()

    output = tmp_path / "prompt.md"

    result = runner.invoke(
        main,
        [
            str(tmp_path),
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0

    assert output.exists()

def test_cli_writes_output_file(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        "print('Hello')",
        encoding="utf-8",
    )

    output = tmp_path / "prompt.md"

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            str(tmp_path),
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0

    assert output.exists()

    content = output.read_text(
        encoding="utf-8",
    )

    assert "main.py" in content

def test_gitignore_is_used_by_default(tmp_path: Path):
    project = tmp_path

    (project / ".git").mkdir()

    (project / ".gitignore").write_text(
        "secret.txt\n",
        encoding="utf-8",
    )

    (project / "secret.txt").write_text(
        "hidden",
        encoding="utf-8",
    )

    (project / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(project)],
    )

    assert result.exit_code == 0

    assert "main.py" in result.output
    assert "## secret.txt" not in result.output

def test_no_gitignore_option_disables_gitignore_filter(tmp_path: Path):
    project = tmp_path

    (project / ".git").mkdir()

    (project / ".gitignore").write_text(
        "secret.txt\n",
        encoding="utf-8",
    )

    (project / "secret.txt").write_text(
        "hidden",
        encoding="utf-8",
    )

    (project / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            str(project),
            "--no-gitignore",
        ],
    )

    assert result.exit_code == 0

    assert "## main.py" in result.output
    assert "## secret.txt" in result.output

def test_main_ignores_files_matching_single_pattern(tmp_path: Path) -> None:
    main_file = tmp_path / "main.py"
    main_file.write_text('print("Hello")\n', encoding="utf-8")

    csv_file = tmp_path / "data.csv"
    csv_file.write_text("id,name\n1,test\n", encoding="utf-8")

    runner = CliRunner()

    result = runner.invoke(
        main,
        [str(tmp_path), "--ignore", "*.csv"],
    )

    assert result.exit_code == 0

    assert "main.py" in result.output
    assert 'print("Hello")' in result.output

    assert "data.csv" not in result.output
    assert "id,name" not in result.output


def test_main_ignores_files_matching_multiple_patterns(tmp_path: Path) -> None:
    main_file = tmp_path / "main.py"
    main_file.write_text('print("Hello")\n', encoding="utf-8")

    csv_file = tmp_path / "data.csv"
    csv_file.write_text("id,name\n1,test\n", encoding="utf-8")

    log_file = tmp_path / "app.log"
    log_file.write_text("INFO: started\n", encoding="utf-8")

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            str(tmp_path),
            "--ignore",
            "*.csv",
            "-i",
            "*.log",
        ],
    )

    assert result.exit_code == 0

    assert "main.py" in result.output
    assert "data.csv" not in result.output
    assert "app.log" not in result.output


def test_main_ignore_works_alongside_no_gitignore(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()

    (tmp_path / ".gitignore").write_text("secret.txt\n", encoding="utf-8")
    (tmp_path / "secret.txt").write_text("hidden", encoding="utf-8")
    (tmp_path / "temp.log").write_text("log content", encoding="utf-8")
    (tmp_path / "main.py").write_text("print('hello')", encoding="utf-8")

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            str(tmp_path),
            "--no-gitignore",
            "--ignore",
            "*.log",
        ],
    )

    assert result.exit_code == 0

    assert "## secret.txt" in result.output
    assert "temp.log" not in result.output
    assert "main.py" in result.output


def test_build_filter_pipeline_adds_pattern_filter_when_ignore_patterns_present(tmp_path: Path) -> None:
    config = PromptForgeConfig(
        use_gitignore=False,
        ignore_patterns=["*.csv", "*.log"],
    )

    pipeline = _build_filter_pipeline(config, tmp_path, None)

    assert len(pipeline._filters) == 1
    assert isinstance(pipeline._filters[0], PatternFilter)


def test_build_filter_pipeline_empty_when_no_filters_active(tmp_path: Path) -> None:
    config = PromptForgeConfig(
        use_gitignore=False,
        ignore_patterns=[]
    )

    pipeline = _build_filter_pipeline(config, tmp_path, None)

    assert len(pipeline._filters) == 0

def test_main_tree_only_outputs_only_project_tree(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            str(tmp_path),
            "--tree-only",
        ],
    )

    assert result.exit_code == 0

    assert "main.py" in result.output
    assert 'print("Hello")' not in result.output
    assert "## main.py" not in result.output

def test_main_content_only_outputs_only_file_contents(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        'print("Hello")\n',
        encoding="utf-8",
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            str(tmp_path),
            "--content-only",
        ],
    )

    assert result.exit_code == 0

    assert "## main.py" in result.output
    assert 'print("Hello")' in result.output

    assert "├──" not in result.output
    assert "└──" not in result.output

@pytest.mark.parametrize(
    "tree_only, content_only, expected_tree, expected_content",
    [
        (False, False, True, True),
        (True, False, True, False),
        (False, True, False, True),
    ],
)
def test_build_prompt_forge(
    tree_only: bool,
    content_only: bool,
    expected_tree: bool,
    expected_content: bool,
) -> None:
    config = PromptForgeConfig(
        use_gitignore=True,
        ignore_patterns=[],
        tree_only=tree_only,
        content_only=content_only,
    )

    builder = _build_prompt_forge(config)

    assert builder.build_tree is expected_tree
    assert builder.build_content is expected_content