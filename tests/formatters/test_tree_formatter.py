from pathlib import Path

from promptforge.formatters.tree_formatter import TreeFormatter
from promptforge.models.project_file import ProjectFile
from promptforge.models.project_diretory import ProjectDirectory
from promptforge.models.tree_node import TreeNode


def test_format_empty_tree(tmp_path: Path) -> None:
    tree = TreeNode(
        ProjectDirectory(tmp_path)
    )

    result = TreeFormatter().format(tree)

    assert result == tmp_path.name

def test_format_root_files(tmp_path: Path) -> None:
    root = TreeNode(
        ProjectDirectory(tmp_path),
        children=[
            TreeNode(
                ProjectDirectory(tmp_path / "src")
            ),
            TreeNode(
                ProjectFile(tmp_path / "README.md")
            ),
        ],
    )

    result = TreeFormatter().format(root)

    assert result == "\n".join([
        tmp_path.name,
        "├── src",
        "└── README.md",
    ])

def test_format_nested_directories(tmp_path: Path) -> None:
    src = tmp_path / "src"
    promptforge = src / "promptforge"

    tree = TreeNode(
        ProjectDirectory(tmp_path),
        children=[
            TreeNode(
                ProjectDirectory(src),
                children=[
                    TreeNode(
                        ProjectDirectory(promptforge),
                        children=[
                            TreeNode(
                                ProjectFile(
                                    promptforge / "cli.py"
                                )
                            )
                        ],
                    )
                ],
            )
        ],
    )

    result = TreeFormatter().format(tree)

    assert result == "\n".join([
        tmp_path.name,
        "└── src",
        "    └── promptforge",
        "        └── cli.py",
    ])

from promptforge.scanner.scanner import Scanner
from promptforge.tree.tree_builder import TreeBuilder


def test_format_tree_builder_result(tmp_path: Path) -> None:
    (tmp_path / "README.md").touch()

    src = tmp_path / "src"
    src.mkdir()

    (src / "main.py").touch()
    (src / "utils.py").touch()

    scan_result = Scanner().scan(tmp_path)
    tree = TreeBuilder().build(scan_result)

    result = TreeFormatter().format(tree)

    assert result == "\n".join([
        tmp_path.name,
        "├── src",
        "│   ├── main.py",
        "│   └── utils.py",
        "└── README.md",
    ])

def test_format_complex_project(tmp_path: Path) -> None:
    src = tmp_path / "src"
    promptforge = src / "promptforge"
    filters = promptforge / "filters"
    scanner = promptforge / "scanner"
    utils = src / "utils"

    filters.mkdir(parents=True)
    scanner.mkdir(parents=True)
    utils.mkdir(parents=True)

    (filters / "gitignore_filter.py").touch()
    (filters / "path_filter.py").touch()
    (scanner / "scanner.py").touch()

    (utils / "parser.py").touch()
    (utils / "reader.py").touch()

    tests = tmp_path / "tests"
    test_filters = tests / "filters"
    test_scanner = tests / "scanner"

    test_filters.mkdir(parents=True)
    test_scanner.mkdir(parents=True)

    (test_filters / "test_gitignore_filter.py").touch()
    (test_scanner / "test_scanner.py").touch()

    (tmp_path / "README.md").touch()

    scan_result = Scanner().scan(tmp_path)
    tree = TreeBuilder().build(scan_result)

    result = TreeFormatter().format(tree)

    assert result == "\n".join([
        tmp_path.name,
        "├── src",
        "│   ├── promptforge",
        "│   │   ├── filters",
        "│   │   │   ├── gitignore_filter.py",
        "│   │   │   └── path_filter.py",
        "│   │   └── scanner",
        "│   │       └── scanner.py",
        "│   └── utils",
        "│       ├── parser.py",
        "│       └── reader.py",
        "├── tests",
        "│   ├── filters",
        "│   │   └── test_gitignore_filter.py",
        "│   └── scanner",
        "│       └── test_scanner.py",
        "└── README.md",
    ])