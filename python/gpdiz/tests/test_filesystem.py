# -*- coding: utf-8 -*-
from __future__ import print_function
from pathlib import Path
import pytest
from gpdiz.treewalker import TreeWalker
from gpdiz.libfile import LibFile
from gpdiz.flacfile import FlacFile

source_dp: Path = Path("/Users/jeremy/Code/gpdiz/source/Music")
source_fp: Path = Path("/Users/jeremy/Code/gpdiz/source/Music/Rock/Gentle Giant")
sourcedir: Path = Path("/Users/jeremy/Code/gpdiz/source")
targetdir: Path = Path("/Users/jeremy/Code/gpdiz/target")

class Test_walks(object):
    def test_walkfiles(self):
        print()
        tw = TreeWalker()
        for item in tw.files(root=source_fp):
            print(item)
        assert True

    def test_walkdirs(self):
        print()
        tw = TreeWalker()
        for item in tw.dirs(root=source_dp):
            print(item)
        assert True

    def test_walkemptydirs(self):
        print()
        tw = TreeWalker()
        for item in tw.empty_dirs(root=source_dp):
            print(item)
        assert True

class Test_foster(object):
    def test_adoption(self):
        tw = TreeWalker()
        for item in tw.files(root=source_fp):
            lf = LibFile(src=item)
            print(f"{str(lf)} ---> ")
            ff:FlacFile = FlacFile(sbj=lf)
            print(str(ff))
            outp = lf.transplant(root=sourcedir,dest=targetdir)
            print(f" ---> {str(outp)}")