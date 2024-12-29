# -*- coding: utf-8 -*-
"""
App for library-level CLI calls
"""
# from pathlib import Path
# from typing import List
from typing_extensions import Annotated

import typer


app = typer.Typer()


@app.command()
def sine_tone(
    dest: Annotated[str, typer.Argument(help="Target file")],
) -> None:
    """
    Command for generating a single mono sine tone.
    """
    print(dest)
