# -*- coding: utf-8 -*-
"""
Ops for library-level translation/copy calls
"""
import shutil
import subprocess
from pathlib import Path

from typing import Dict, List
from .libfile import LibFile
from .flacfile import FlacFile


# pylint: disable=too-few-public-methods
class Factory:
    """
    Factory class for aggregating intelligent methods for translation and copying
    """

    def __init__(self):
        self._default_bitrate = "320k"
        self._special_bitrates: Dict[str, str] = {"Book": "128k"}

    def _copy(self, inp: LibFile, outp: LibFile) -> None:
        """
        Implements a straight-through copy
        """
        if not outp.exists:
            outp.parent.mkdir(parents=True, exist_ok=True)
        # print(f"   copying:\n  {str(inp.path)}\n  {str(outp.path)}")
        shutil.copy(src=inp.path, dst=outp.path)

    def _convert_playlist(self, inp: LibFile, outp: LibFile) -> None:
        """
        Changes relative paths from flac to mp3 in playlist file
        """
        if not outp.exists:
            outp.parent.mkdir(parents=True, exist_ok=True)
        # print(f"  playlist:\n  {str(inp.path)}\n  {str(outp.path)}")
        with open(inp.path, "r", encoding="utf8") as infile:
            intext: str = infile.read()
        outext: str = intext.replace(".flac", ".mp3")
        with open(outp.path, "w", encoding="utf8") as outfile:
            outfile.write(outext)

    def _convert_to_mp3(
        self, inp: LibFile, outp: LibFile, bitrate: str = "320k"
    ) -> None:
        """
        Implements a format conversion to MP3
        """
        inf = str(inp.path)
        tmpf = Path("/tmp", outp.name)
        if tmpf.exists():
            tmpf.unlink()

        cmd = [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-i",
            inf,
            "-b:a",
            bitrate,
            "-map_metadata",
            "0",
            "-id3v2_version",
            "3",
            str(tmpf),
        ]
        # print(f"converting:\n  {str(inp.path)}\n  {str(outp.path)}    at {bitrate}")
        subprocess.run(cmd, check=True)
        if not outp.exists:
            outp.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src=tmpf, dst=outp.path)
        tmpf.unlink()

    def _estimate_mp3_bitrate(self, inp: LibFile):
        retval: str = self._default_bitrate
        flfl: FlacFile = FlacFile(sbj=inp)
        if flfl.genre in self._special_bitrates:
            retval = self._special_bitrates[flfl.genre]
        return retval

    def translate(self, inp: LibFile, outp: LibFile, playlist: bool = False):
        """
        Factory input call to intelligently process the input and output according
        to their file type requirements
        """
        inflac: bool = False
        outmp3: bool = False

        if inp.suffix == ".flac":
            inflac = True

        if outp.suffix == ".mp3":
            outmp3 = True

        if inflac and outmp3:
            brate: str = self._estimate_mp3_bitrate(inp=inp)
            self._convert_to_mp3(inp=inp, outp=outp, bitrate=brate)
        else:
            if inp.suffix == ".m3u" and playlist:
                self._convert_playlist(inp=inp, outp=outp)
            else:
                self._copy(inp=inp, outp=outp)

    def prune(self, sample: LibFile, masters: List[LibFile]):
        """
        Remove obsolete copied/generated files.
        """
        keep: bool = False
        for item in masters:
            if item.exists:
                keep = True
        if not keep:
            sample.path.unlink()
