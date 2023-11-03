import typer
from typing_extensions import Annotated
from typing import Optional

from huggingface import changelog_hugging
from parse import parse


def main(
    git_dir: Annotated[
        Optional[str], typer.Argument(help="Git repository directory")
    ] = None,
    changelog_dir: Annotated[
        Optional[str], typer.Argument(help="Changelog directory")
    ] = None,
):
    text = changelog_hugging(git_dir)
    parse(text, changelog_dir)


if __name__ == "__main__":
    typer.run(main)
