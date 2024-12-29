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
        self._mdata: Dict[str, Any] = {}
        self._mdata["valid"] = False
        self._mdata["hires"] = False
        if (self._sbj.exists) and (self._sbj.suffix == ".flac"):
            self._mdata["valid"] = True
        if self._mdata["valid"]:
            self._flac: FLAC = FLAC(self._sbj.path)
            _info: StreamInfo = self._flac.info
            self._mdata["sample_rate"] = _info.sample_rate
            self._mdata["bits_per_sample"] = _info.bits_per_sample
            self._mdata["channels"] = _info.channels
            self._mdata["bitrate"] = _info.bitrate
            if (self._mdata["bits_per_sample"] > 16) or (
                self._mdata["sample_rate"] > 44100
            ):
                self._mdata["hires"] = True
            self._mdata["genre"] = str(self._flac["GENRE"][0])

    @property
    def valid(self):
        """Accessor"""
        return self._mdata["valid"]

    @property
    def sample_rate(self) -> int:
        """Accessor"""
        if self.valid:
            return self._mdata["sample_rate"]
        return -1

    @property
    def bits_per_sample(self) -> int:
        """Accessor"""
        if self.valid:
            return self._mdata["bits_per_sample"]
        return -1

    @property
    def channels(self) -> int:
        """Accessor"""
        if self.valid:
            return self._mdata["channels"]
        return -1

    @property
    def bitrate(self) -> int:
        """Accessor"""
        if self.valid:
            return self._mdata["bitrate"]
        return -1

    @property
    def hires(self) -> bool:
        """Accessor"""
        if self.valid:
            return self._mdata["hires"]
        return False

    @property
    def genre(self) -> str:
        """Accessor"""
        if self.valid:
            return self._mdata["genre"]
        return "NULL"

    def debug(self):
        """
        Debugger
        """
        print(self._flac.pprint())

    def __str__(self) -> str:
        return json.dumps(self._mdata)
