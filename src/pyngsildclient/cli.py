"""Console script for pyngsildclient."""

import typer
from rich.console import Console

from pyngsildclient import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for pyngsildclient."""
    console.print("Replace this message by putting your code into pyngsildclient.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
