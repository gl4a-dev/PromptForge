from pathlib import Path
import click

from promptforge.cli.config import PromptForgeConfig
from promptforge.cli.writer import PromptWriter
from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.filters.pipline import FilterPipeline
from promptforge.filters.filter import Filter
from promptforge.filters.gitignore_filter import GitIgnoreFilter
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
    "-o",
    "--output",
    type=click.Path(
        dir_okay=False,
        path_type=Path,
    ),
    help="Write the generated prompt to a UTF-8 file.",
)
@click.option(
    "--no-gitignore",
    is_flag=True,
    help="Do not apply .gitignore rules.",
)
def main(
    path: Path,
    output: Path | None,
    no_gitignore: bool,
) -> None:
    """Generate a prompt from a project."""

    config = PromptForgeConfig(
        use_gitignore=not no_gitignore
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