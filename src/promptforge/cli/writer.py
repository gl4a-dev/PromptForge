from pathlib import Path

import click


class PromptWriter:

    @staticmethod
    def write(
        prompt: str,
        output: Path | None,
    ) -> None:

        if output is None:
            click.echo(prompt)
            return

        output.write_text(
            prompt,
            encoding="utf-8",
        )