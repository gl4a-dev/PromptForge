from pathlib import Path

from promptforge.git.repository import GitRepository


def test_discover_returns_scan_root_when_not_git_repository(tmp_path: Path):
    root = GitRepository.discover(tmp_path)

    assert root == tmp_path.resolve()

def test_discover_git_root(tmp_path: Path):
    (tmp_path / ".git").mkdir()

    root = GitRepository.discover(tmp_path)

    assert root == tmp_path.resolve()

def test_discover_git_root_from_child_directory(tmp_path: Path):
    (tmp_path / ".git").mkdir()

    project = tmp_path / "backend"
    project.mkdir()

    root = GitRepository.discover(project)

    assert root == tmp_path.resolve()

def test_discover_git_root_from_nested_directory(tmp_path: Path):
    (tmp_path / ".git").mkdir()

    nested = (
        tmp_path
        / "backend"
        / "services"
        / "billing"
    )

    nested.mkdir(parents=True)

    root = GitRepository.discover(nested)

    assert root == tmp_path.resolve()

def test_discover_without_git_returns_original_scan_root(tmp_path: Path):
    nested = (
        tmp_path
        / "backend"
        / "services"
    )

    nested.mkdir(parents=True)

    root = GitRepository.discover(nested)

    assert root == nested.resolve()