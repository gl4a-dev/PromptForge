from pathlib import Path

from promptforge.scanner.scanner import Scanner
from promptforge.models.tree_node import TreeNode
from promptforge.tree.tree_builder import TreeBuilder


def _find_child(node: TreeNode, name: str) -> TreeNode:
    return next(
        child
        for child in node.children
        if child.entry.path.name == name
    )

def test_single_file(tmp_path: Path) -> None:
    (tmp_path / "README.md").touch()

    scan = Scanner().scan(tmp_path)

    tree = TreeBuilder().build(scan)

    assert tree.entry.path == tmp_path.resolve()

    assert len(tree.children) == 1
    assert tree.children[0].entry.path.name == "README.md"

def test_directory_structure(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    (src / "main.py").touch()
    (src / "utils.py").touch()

    tree = TreeBuilder().build(
        Scanner().scan(tmp_path)
    )

    src_node = _find_child(tree, "src")

    assert len(src_node.children) == 2

    assert {
        child.entry.path.name
        for child in src_node.children
    } == {
        "main.py",
        "utils.py",
    }

def test_nested_directories(tmp_path: Path) -> None:
    package = tmp_path / "src" / "promptforge"
    package.mkdir(parents=True)

    (package / "cli.py").touch()

    tree = TreeBuilder().build(
        Scanner().scan(tmp_path)
    )

    src = _find_child(tree, "src")
    promptforge = _find_child(src, "promptforge")
    cli = _find_child(promptforge, "cli.py")

    assert cli.entry.path.name == "cli.py"

def test_directories_are_sorted_before_files(tmp_path: Path) -> None:
    (tmp_path / "b.py").touch()
    (tmp_path / "a.py").touch()

    (tmp_path / "src").mkdir()
    (tmp_path / "docs").mkdir()

    tree = TreeBuilder().build(
        Scanner().scan(tmp_path)
    )

    names = [
        child.entry.path.name
        for child in tree.children
    ]

    assert names == [
        "docs",
        "src",
        "a.py",
        "b.py",
    ]

def test_empty_project(tmp_path: Path) -> None:
    tree = TreeBuilder().build(
        Scanner().scan(tmp_path)
    )

    assert tree.entry.path == tmp_path.resolve()

    assert tree.children == []

def test_tree_contains_all_scanned_entries(tmp_path: Path) -> None:
    (tmp_path / "README.md").touch()

    src = tmp_path / "src"
    src.mkdir()

    (src / "main.py").touch()

    tests = tmp_path / "tests"
    tests.mkdir()

    (tests / "test_main.py").touch()

    scan_result = Scanner().scan(tmp_path)

    tree = TreeBuilder().build(scan_result)

    found = {
        node.entry.path.name
        for node in tree.walk()
    }

    assert found == {
        tmp_path.name,
        "README.md",
        "src",
        "main.py",
        "tests",
        "test_main.py",
    }

def test_walk_is_depth_first(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()

    package = src / "promptforge"
    package.mkdir()

    (package / "cli.py").touch()
    (tmp_path / "README.md").touch()

    tree = TreeBuilder().build(
        Scanner().scan(tmp_path)
    )

    names = [
        node.entry.path.name
        for node in tree.walk()
    ]

    assert names == [
        tmp_path.name,
        "src",
        "promptforge",
        "cli.py",
        "README.md",
    ]


