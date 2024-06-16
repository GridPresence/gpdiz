# -*- coding: utf-8 -*-
"""
Command execution environment for CLI apps in Python
"""
import typer
from . import library

app = typer.Typer(add_completion=False)

app.add_typer(library.app, name="lib", help="Library tools")


def main():
    """
    Entry point
    """
    app()


if __name__ == "__main__":
    typer.run(main)
