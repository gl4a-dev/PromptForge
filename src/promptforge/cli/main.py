from pathlib import Path
import click

from promptforge.cli.config import PromptForgeConfig
from promptforge.cli.writer import PromptWriter
from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.filters.pipline import FilterPipeline
from promptforge.filters.filter import Filter
from promptforge.filters.gitignore_filter import GitIgnoreFilter
from promptforge.filters.pattern_filter import PatternFilter
from promptforge.git.repository import GitRepository
from promptforge.scanner.scanner import Scanner


def _build_filter_pipeline(
    config: PromptForgeConfig, 
    scan_root: Path, 
    git_root: Path | None
) -> FilterPipeline:
    filters: list[Filter] = []

    if config.use_gitignore:
        filters.append(
            GitIgnoreFilter(
                scan_root,
                git_root,
            )
        )

    if config.ignore_patterns:
        filters.append(
            PatternFilter(
                scan_root,
                config.ignore_patterns,
            )
        )

    return FilterPipeline(filters)


@click.command()
@click.argument(
    "path",
    type=click.Path(
        path_type=Path,
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    default=".",
)
@click.option(
    "--no-gitignore",
    is_flag=True,
    help="Do not apply .gitignore rules.",
)
@click.option(
    "--ignore",
    "-i",
    multiple=True, 
    type=str,
    help="Ignore additional file patterns.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(
        dir_okay=False,
        path_type=Path,
    ),
    help="Write the generated prompt to a UTF-8 file.",
)
def main(
    path: Path,
    no_gitignore: bool,
    ignore,
    output: Path | None,
) -> None:
    """Generate a prompt from a project."""

    config = PromptForgeConfig(
        use_gitignore=not no_gitignore,
        ignore_patterns=list(ignore)
    )

    scanner = Scanner()
    scan_result = scanner.scan(path)

    scan_root = path.resolve()
    git_root = GitRepository.discover(scan_root)

    pipeline = _build_filter_pipeline(
        config,
        scan_root,
        git_root,
    )

    filtered_result = pipeline.apply(scan_result)

    prompt = PromptBuilder().build(filtered_result)

    PromptWriter.write(
        prompt,
        output,
    )


if __name__ == "__main__":
    main()