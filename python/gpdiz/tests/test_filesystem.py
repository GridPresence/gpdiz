# -*- coding: utf-8 -*-
from __future__ import print_function
from pathlib import Path
import pytest
from gpdiz.treewalker import TreeWalker
from gpdiz.libfile import LibFile
from gpdiz.flacfile import FlacFile
from gpdiz.factory import FileFactory

source_dp: Path = Path("/Users/jeremy/Code/gpdiz/source/Music")
source_fp: Path = Path("/Users/jeremy/Code/gpdiz/source/Music/Rock/Gentle Giant")
sourcedir: Path = Path("/Users/jeremy/Code/gpdiz/source")
targetdir: Path = Path("/Users/jeremy/Code/gpdiz/target")
soure_translate: Path = Path(
    "/Users/jeremy/Code/gpdiz/source/Music/Books/Banks, Iain M/1993 - Against a Dark Background {Peter Kenny}"
)
target_translate: Path = Path(
    "/Users/jeremy/Code/gpdiz/target/Music/Books/Banks, Iain M"
)


class Test_walks(object):
    def test_walkfiles(self):
        # print()
        tw = TreeWalker()
        for item in tw.files(root=source_fp):
            # print(item)
            assert item == item

    def test_walkdirs(self):
        print()
        tw = TreeWalker()
        for item in tw.dirs(root=source_dp):
            # print(item)
            assert item == item

    def test_walkemptydirs(self):
        # print()
        tw = TreeWalker()
        for item in tw.empty_dirs(root=source_dp):
            # print(item)
            assert item == item


class Test_foster(object):
    def test_adoption(self):
        tw = TreeWalker()
        for item in tw.files(root=source_fp):
            lf = LibFile(src=item)
            # print(f"{str(lf)} ---> ")
            ff: FlacFile = FlacFile(sbj=lf)
            # print(str(ff))
            outp = lf.transplant(root=sourcedir, dest=targetdir)
            # print(f" ---> {str(outp)}")


class Test_translate(object):
    def test_speech_translator(self):
        factory: FileFactory = FileFactory()
        tw = TreeWalker()
        for item in tw.files(root=soure_translate):
            lf = LibFile(src=item)
            if item.suffix in [".flac"]:
                newitem = lf.transplant(
                    root=soure_translate, dest=target_translate, fmt=".mp3"
                )
            else:
                newitem = lf.transplant(root=soure_translate, dest=target_translate)
            nf = LibFile(src=newitem)
            if nf.exists:
                if nf.modified < lf.modified:
                    factory.translate(inp=lf, outp=nf, playlist=True)
            else:
                factory.translate(inp=lf, outp=nf, playlist=True)
