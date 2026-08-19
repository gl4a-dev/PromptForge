import pytest

from promptforge.cli.config import PromptForgeConfig


def test_default_config():
    config = PromptForgeConfig()

    assert config.use_gitignore is True
    assert config.ignore_patterns == []
    assert config.include_patterns == []
    assert config.tree_only is False
    assert config.content_only is False
    assert config.max_file_size is None

def test_custom_config():
    config = PromptForgeConfig(
        use_gitignore=False,
        ignore_patterns=["*.csv"],
        include_patterns=["*.py"],
        tree_only=True,
        max_file_size=1024,
    )

    assert config.use_gitignore is False
    assert config.ignore_patterns == ["*.csv"]
    assert config.include_patterns == ["*.py"]
    assert config.tree_only is True
    assert config.content_only is False
    assert config.max_file_size == 1024

def test_tree_only_and_content_only_are_mutually_exclusive():
    with pytest.raises(ValueError):
        PromptForgeConfig(
            tree_only=True,
            content_only=True,
        )