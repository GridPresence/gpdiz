# -*- coding: utf-8 -*-
"""
App for library-level CLI calls
"""
from pathlib import Path
from typing import List
from typing_extensions import Annotated

import typer

from .libfile import LibFile
from .treewalker import TreeWalker
from .flacfile import FlacFile
from .factory import FileFactory

app = typer.Typer()


@app.command()
def shift_mp3(
    source: Annotated[str, typer.Argument(help="Source directory")],
    destination: Annotated[str, typer.Argument(help="Target directory")],
) -> None:
    """
    Command for lifting and converting a mixed format library into a
    corresponding MP3 library suitable for use in a DAP.
    """
    src = Path(source)
    dst = Path(destination)
    factory: FileFactory = FileFactory()
    tw = TreeWalker()
    for item in tw.files(root=Path(source)):
        lf = LibFile(src=item)
        if item.suffix in [".flac"]:
            newitem = lf.transplant(root=src, dest=dst, fmt=".mp3")
        else:
            newitem = lf.transplant(root=src, dest=dst)
        nf = LibFile(src=newitem)
        if nf.exists:
            if nf.modified < lf.modified:
                factory.translate(inp=lf, outp=nf, playlist=True)
        else:
            factory.translate(inp=lf, outp=nf, playlist=True)


@app.command()
def shift_hr_flac(
    source: Annotated[str, typer.Argument(help="Source directory")],
    destination: Annotated[str, typer.Argument(help="Destination directory")],
) -> None:
    """
    Command for lifting HR FLAC directories into an
    exclusively HR library suitable for use in a high-end DAP.
    """
    src = Path(source)
    dst = Path(destination)
    tw = TreeWalker()
    dirs: List[str] = []
    for item in tw.files(root=src):
        tmp = str(item.parent)
        if tmp not in dirs:
            if item.suffix in [".flac"]:
                ff = FlacFile(sbj=LibFile(src=item))
                if ff.hires:
                    print(f"stack: {tmp}")
                    dirs.append(tmp)
    factory: FileFactory = FileFactory()
    for item2 in tw.targeted_files(targets=dirs):
        print(f" copy: {str(item2)}")
        lf = LibFile(src=item2)
        newitem = lf.transplant(root=src, dest=dst)
        nf = LibFile(src=newitem)
        if nf.exists:
            if nf.modified < lf.modified:
                factory.translate(inp=lf, outp=nf)
        else:
            factory.translate(inp=lf, outp=nf)


@app.command()
def prune_mp3(
    source: Annotated[str, typer.Argument(help="Source directory")],
    master: Annotated[str, typer.Argument(help="Master directory")],
) -> None:
    """
    Command for pruning MP3 directories where the master source
    has been moved/deleted.
    """
    src = Path(source)
    mst = Path(master)
    tw = TreeWalker()
    mstitems: List[LibFile] = []
    factory: FileFactory = FileFactory()
    for item in tw.files(root=src):
        mstitems = []
        lf = LibFile(src=item)
        mstitems.append(LibFile(lf.transplant(root=src, dest=mst)))
        if lf.suffix == ".mp3":
            mstitems.append(LibFile(lf.transplant(root=src, dest=mst, fmt=".flac")))
        factory.prune(sample=lf, masters=mstitems)
    stack: List[Path] = []
    while True:
        stack = []
        ntw = TreeWalker()
        for item in ntw.empty_dirs(root=src):
            stack.append(item)
        if stack:
            # print("")
            for pth in stack:
                # print(str(pth))
                pth.rmdir()
        else:
            break
