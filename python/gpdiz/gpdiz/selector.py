# -*- coding: utf-8 -*-
"""
Module docstring
"""
import json
from pathlib import Path


class Selector:

    def __init__(self, Path: spec):
        self._src = None
        self._trg = None
        self._selects = None
        self._spec: Path = spec
        self._sourceset = None
        self._targetset = None

        self._readSpecs()
        self._buildSourceSet()
        self._buildTargetSet()
        self._buildDeleteSet()
        self._buildCopySet()

    def _readSpecs(self):
        if self._spec is not None:
            with open(self._spec) as fp:
                data = json.load(fp)
                self._src = data["source"]

                # print(self._src)
                self._trg = data["target"]
                # print(self._trg)
                self._selects = data["selections"]
                # print(self._selects)

    def _buildSourceSet(self):
        stree = Tree()
        for band in self._selects:
            if self._selects[band][0] == "*":
                # path = '{0}/{1}'.format(self._src, band)
                # print(band)
                stree.walk(spath=self._src, match=band)
            else:
                stree.postfix_scan(spath=self._src, subpath=band, filt=".m3u")
                for album in self._selects[band]:
                    path = "{0}/{1}".format(band, album)
                    stree.walk(spath=self._src, match=path)
        # print(stree)
        self._sourceset = stree._data

    def _buildCopySet(self):
        self._copyset = self._sourceset.difference(self._targetset)
        # print(self._copyset)
        self._copySet()

    def _copySet(self):
        for item in self._copyset:
            src = Path(self._src) / item
            trg = Path(self._trg) / item
            mkdir_p(str(trg.parent))
            print(item)
            copyfile(str(src), str(trg))

    def _buildDeleteSet(self):
        self._deleteset = self._targetset.difference(self._sourceset)
        # print(self._deleteset)
        self._deleteSet()

    def _deleteSet(self):
        for item in self._deleteset:
            dispose = Path(self._trg) / item
            # print(dispose)
            dispose.unlink()
        treetop = Path(self._trg)
        for direct in treetop.iterdir():
            if direct.is_dir() is True:
                for direct2 in direct.iterdir():
                    # print(direct2)
                    try:
                        direct2.rmdir()
                    except OSError:
                        pass
                print(direct)
                try:
                    direct.rmdir()
                except OSError:
                    pass
