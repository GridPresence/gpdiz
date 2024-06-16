# -*- coding: utf-8 -*-
"""
Utility classes and methods for manipulating the filesystem
"""
# import tempfile
from typing import Iterator, List
from pathlib import Path

# from typing import List


class TreeWalker:
    """
    Generators for walking down filesystem directory trees
    """

    def files(self, root: Path) -> Iterator[Path]:
        """
        Generator function that walks a directory tree and emits
        the path of each of the files therein.
        """
        for path in root.iterdir():
            if path.is_dir():
                yield from self.files(path)
                continue
            # We don't care about Mac OS Finder cruft
            if path.name == ".DS_Store":
                path.unlink()
            else:
                yield path.resolve()

    def targeted_files(self, targets: List[str]) -> Iterator[Path]:
        """
        Generator function that walks a list of directory trees and emits
        the path of each of the files therein.
        """
        for tdir in targets:
            troot = Path(tdir).resolve()
            for path in troot.iterdir():
                if path.is_dir():
                    yield from self.files(path)
                    continue
                # We don't care about Mac OS Finder cruft
                if path.name == ".DS_Store":
                    path.unlink()
                else:
                    yield path.resolve()

    def dirs(self, root: Path) -> Iterator[Path]:
        """
        Generator function that walks a directory tree and emits
        the path of each of the directories therein.
        """
        for path in root.iterdir():
            if path.is_dir():
                yield path.resolve()
                yield from self.dirs(path)
                continue

    def empty_dirs(self, root: Path) -> Iterator[Path]:
        """
        Generator function that walks a directory tree and emits
        the path of each of the empty directories therein.
        """
        for path in root.iterdir():
            # print(str(path))
            if path.is_dir():
                # print(f"    {str(path)}")
                if not any(path.iterdir()):
                    # print(f"        {str(path.resolve())}")
                    yield path.resolve()
                yield from self.empty_dirs(path)
                continue
