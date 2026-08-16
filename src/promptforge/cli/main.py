from pathlib import Path
import click

from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.filters.gitignore_filter import GitIgnoreFilter
from promptforge.git.repository import GitRepository
from promptforge.filters.pipline import FilterPipeline
from promptforge.scanner.scanner import Scanner
from promptforge.cli.writer import PromptWriter


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
def main(path: Path, output: Path | None) -> None:
    """Generate a prompt from a project."""

    scanner = Scanner()
    scan_result = scanner.scan(path)

    scan_root = path.resolve()
    git_root = GitRepository.discover(scan_root)

    pipeline = FilterPipeline([
        GitIgnoreFilter(
            scan_root,
            git_root,
        ),
    ])

    filtered_result = pipeline.apply(scan_result)

    prompt = PromptBuilder().build(filtered_result)

    PromptWriter.write(
        prompt,
        output,
    )


if __name__ == "__main__":
    main()