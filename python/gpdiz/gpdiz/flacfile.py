# -*- coding: utf-8 -*-
"""
Utility classes and methods for manipulating FLAC files
"""
# from pathlib import Path
from typing import Dict, Any
import json
from mutagen.flac import FLAC, StreamInfo
from .libfile import LibFile


# pylint: disable=too-few-public-methods
class FlacFile:
    """Wrapper class"""

    def __init__(self, sbj: LibFile):
        self._sbj: LibFile = sbj
        self._valid: bool = False
        self._hires: bool = False
        self._genre: str = ""
        if (self._sbj.exists) and (self._sbj.suffix == ".flac"):
            self._valid = True
        if self._valid:
            self._flac: FLAC = FLAC(self._sbj.path)
            self._info: StreamInfo = self._flac.info
            if (self.bits_per_sample > 16) or (self.sample_rate > 44100):
                self._hires = True
            self._genre = str(self._flac["GENRE"][0])

    @property
    def sample_rate(self) -> int:
        """Accessor"""
        if self._valid:
            return self._info.sample_rate
        return -1

    @property
    def bits_per_sample(self) -> int:
        """Accessor"""
        if self._valid:
            return self._info.bits_per_sample
        return -1

    @property
    def channels(self) -> int:
        """Accessor"""
        if self._valid:
            return self._info.channels
        return -1

    @property
    def bitrate(self) -> int:
        """Accessor"""
        if self._valid:
            return self._info.bitrate
        return -1

    @property
    def hires(self) -> bool:
        """Accessor"""
        return self._hires

    @property
    def genre(self) -> str:
        """Accessor"""
        return self._genre

    def debug(self):
        """
        Debugger
        """
        print(self._flac.pprint())

    def __str__(self) -> str:
        struct: Dict[str, Any] = {}
        struct["sample_rate"] = self.sample_rate
        struct["bits_per_sample"] = self.bits_per_sample
        struct["hires"] = self.hires
        struct["file"] = self._sbj.name
        struct["modified"] = self._sbj.modified
        struct["size"] = self._sbj.size

        return json.dumps(struct)
