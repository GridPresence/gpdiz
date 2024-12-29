# -*- coding: utf-8 -*-
"""
App for library-level CLI calls
"""
# from pathlib import Path
# from typing import List
from typing_extensions import Annotated

import typer

from .inifile import Profiles


app = typer.Typer()


@app.command()
def set_profile(
    name: Annotated[str, typer.Argument(help="Profile name")],
) -> None:
    """
    Command for setting the default signal profile.
    """
    profs = Profiles()
    # Is this a valid profile name?
    if name not in profs.sections:
        raise ValueError(f"Unknown profile: {name}")
    # Do we have a default section ready to be overwritten?
    if "default" not in profs.sections:
        profs.add_section("default")
    # Copy the named profile section into the default section
    deefault = profs.get_section("default")
    profyle = profs.get_section(name)
    for key, value in profyle.items():
        deefault[key] = value
    # Write the file back
    profs.close()
    print(f"Profile: {name} applied.")
