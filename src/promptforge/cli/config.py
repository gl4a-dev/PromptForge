from dataclasses import dataclass, field


@dataclass(slots=True)
class PromptForgeConfig:
    
    use_gitignore: bool = True

    ignore_patterns: list[str] = field(default_factory=list)
    include_patterns: list[str] = field(default_factory=list)

    tree_only: bool = False
    content_only: bool = False

    max_file_size: int | None = None

    def __post_init__(self) -> None:
        if self.tree_only and self.content_only:
            raise ValueError(
                "'tree_only' and 'content_only' cannot both be enabled."
            )