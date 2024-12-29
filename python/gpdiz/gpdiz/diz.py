# -*- coding: utf-8 -*-
"""
Command execution environment for CLI apps in Python
"""
import typer
from . import library, dsp, dizself, sudoku

app = typer.Typer(add_completion=False)

app.add_typer(library.app, name="lib", help="Library tools")
app.add_typer(dsp.app, name="dsp", help="Signal processing tools")
app.add_typer(dizself.app, name="self", help="Diz-specific utilities")
app.add_typer(sudoku.app, name="sud", help="Sudoku-specific utilities")


def main():
    """
    Entry point
    """
    app()


if __name__ == "__main__":
    typer.run(main)
