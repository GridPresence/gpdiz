# -*- coding: utf-8 -*-
"""
Utility classes and methods for manipulating FLAC files
"""
# from pathlib import Path
from typing import Dict, Any

# import json
# from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from .libfile import LibFile


# pylint: disable=too-few-public-methods
class Mp3Tags:
    """Wrapper class"""

    def __init__(self, sbj: LibFile):
        self._sbj: LibFile = sbj
        self._mdata: Dict[str, Any] = {}
        self._mdata["valid"] = False
        if (self._sbj.exists) and (self._sbj.suffix == ".mp3"):
            self._mdata["valid"] = True
        if self._mdata["valid"]:
            self._info: ID3 = ID3(self._sbj.path)

    def debug(self):
        """Debugger"""
        print(self._info.pprint())
