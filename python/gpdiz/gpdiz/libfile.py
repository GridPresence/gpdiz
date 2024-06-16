# -*- coding: utf-8 -*-
"""
Utility classes and methods for manipulating the filesystem
"""
from pathlib import Path

# from typing import List


class LibFile:
    """
    A description of a library file
    """

    def __init__(self, src: Path):
        self._path: Path = src.resolve()
        self._modified: int = 0
        self._exists: bool = False
        self._size: int = 0
        self.refresh_state()

    def __str__(self) -> str:
        return f"{self._path}: ({self._modified} ... {self._size})"

    @property
    def name(self) -> str:
        """Accessor"""
        return self._path.name

    @property
    def parent(self) -> Path:
        """Accessor"""
        return self._path.parent

    @property
    def path(self) -> Path:
        """Accessor"""
        return self._path

    @property
    def suffix(self) -> str:
        """Accessor"""
        return self._path.suffix

    @property
    def exists(self) -> bool:
        """Accessor"""
        return self._exists

    @property
    def modified(self) -> int:
        """Accessor"""
        return self._modified

    @property
    def size(self) -> int:
        """Accessor"""
        return self._size

    def refresh_state(self):
        """
        Update knowledge about the file state
        """
        self._exists = self._path.exists()
        if self._exists:
            self._modified = int(self._path.stat().st_mtime)
            self._size = self._path.stat().st_size

    def transplant(self, root: Path, dest: Path, fmt: str = ".") -> Path:
        """
        Generate a new path on a dest root.
        """
        # Ensure that the destination spec is absolute
        # and make it the preface for the output path
        retval: Path = dest.resolve()
        # Count the number of terms in the root path
        lenn: int = len(list(root.resolve().parts))
        ctr: int = 0
        for item in list(self._path.parts):
            # Skip the common terms of the root and the file source path
            if ctr >= lenn:
                # Only add the terms below the root path
                retval = retval.joinpath(item)
            ctr += 1
        # Is this transplant going to need a format transformation?
        if fmt != ".":
            retval = retval.with_suffix(fmt)
        return retval.resolve()
