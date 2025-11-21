import sys
from typing import List, Any, Dict
from pathlib import Path
import json
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC


class Scanner:

    CLASSICAL = ["Classical", "Organ", "Choral", "Opera"]
    SPEECH = ["Book", "Drama", "Comedy", "Speech", "Playlists"]

    def __init__(self, source: Path, target: Path, specs: List[str]) -> None:
        self._source: Path = source
        self._target: Path = target
        self._target.mkdir(parents=True, exist_ok=True)
        self._specs: List[str] = []
        self._playlists: Dict[str, Any] = {}
        for item in specs:
            self._specs.append(item)
            # self._playlists[item]: Dict[str, str] = {}

        # print(self._source)
        # print(self._target)
        # print(self._specs)
        # print(self._playlists)

    def _walk(self, spath: Path):
        for path in spath.iterdir():
            if path.is_dir():
                print(path)
                if path.name not in self.SPEECH:
                    yield from self._walk(path)
                continue
            yield path.resolve()

    # def _update(self):
    #     for item in self._playlists:
    #         if self._playlists[item]:
    #             tfnme = f"{item}.m3u"
    #             tfpth = Path(self._target).joinpath(tfnme)
    #             with open(tfpth, "w", encoding="utf8") as tfile:
    #                 tfile.write("#EXTM3U\n")
    #                 for k, v in sorted(self._playlists[item].items()):
    #                     tfile.write(v)
    #             tfile.close()

    # def _tags(self, spath: Path) -> Dict[str, str]:
    #     retval: Dict[str, str] = {}
    #     mpthree = MP3(spath)
    #     idthree = ID3(spath)
    #     # print(idthree.pprint())
    #     retval["length"] = int(mpthree.info.length)
    #     retval["artist"] = idthree["TPE1"].text[0]
    #     retval["disc"] = idthree["TPOS"].text[0]
    #     retval["track"] = idthree["TRCK"].text[0]
    #     try:
    #         retval["date"] = idthree["TDRC"].text[0]
    #     except KeyError:
    #         print(idthree.pprint())
    #         retval["date"] = "1962-12-22"
    #     retval["album"] = idthree["TALB"].text[0]
    #     retval["title"] = idthree["TIT2"].text[0]
    #     retval["genre"] = idthree["TCON"].text[0]
    #     try:
    #         retval["composer"] = idthree["TCOM"].text[0]
    #     except KeyError:
    #         retval["composer"] = "Unknown"
    #     return retval

    def _tags(self, spath: Path) -> Dict[str, str]:
        retval: Dict[str, str] = {}
        mpthree = MP3(spath)
        idthree = ID3(spath)
        # print(idthree.pprint())
        retval["length"] = int(mpthree.info.length)
        retval["artist"] = idthree["TPE1"].text[0]
        retval["disc"] = idthree["TPOS"].text[0]
        retval["track"] = idthree["TRCK"].text[0]
        try:
            retval["date"] = idthree["TDRC"].text[0]
        except KeyError:
            print(idthree.pprint())
            retval["date"] = "1962-12-22"
        retval["album"] = idthree["TALB"].text[0]
        retval["title"] = idthree["TIT2"].text[0]
        retval["genre"] = idthree["TCON"].text[0]
        try:
            retval["composer"] = idthree["TCOM"].text[0]
        except KeyError:
            retval["composer"] = "Unknown"
        return retval

    def scan(self):
        for fyle in self._walk(self._source):
            if fyle.suffix in [".mp3"]:
                tags = self._tags(spath=fyle)
                relpath = Path(fyle).relative_to(self._source)
                finalpath = Path("..", relpath)
                keystr = (
                    f"{tags['date']} {tags['album']} {tags['disc']} {tags['track']}"
                )
                valstr = f"#EXTINF: {tags['length']}, {tags['artist']} - {tags['title']}\n{finalpath}\n"
                if tags["genre"] not in self.SPEECH:
                    if tags["genre"] in self.CLASSICAL:
                        if not tags["composer"] in self._playlists:
                            self._playlists[tags["composer"]]: Dict[str, str] = {}
                        self._playlists[tags["composer"]][keystr] = valstr
                    else:
                        if not tags["artist"] in self._playlists:
                            self._playlists[tags["artist"]]: Dict[str, str] = {}
                        self._playlists[tags["artist"]][keystr] = valstr

        self._update()
