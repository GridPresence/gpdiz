# -*- coding: utf-8 -*-
"""
Module docstring
"""
from math import pi, sin
from typing import List
from .inifile import Profiles


class Signal:
    """
    Utility class for floating point signal representations
    """

    def __init__(self, profname: str = "default"):
        self._profname = profname
        (samp, bdep) = Profiles().content(self._profname)
        self._rate = samp
        self._depth = bdep
        self._size: int = 0
        self._ictr: int = 0
        self._data: List[float] = []

    @property
    def profname(self) -> str:
        """Accessor"""
        return self._profname

    @property
    def rate(self) -> int:
        """Accessor"""
        return self._rate

    @property
    def depth(self) -> int:
        """Accessor"""
        return self._depth

    def extend(self, indat: List[float]):
        """Extender"""
        self._data.extend(indat)

    def append(self, samp: float) -> None:
        """Appender"""
        self._data.append(samp)

    # def __iter__(self):
    #     self._size = len(self._data)
    #     self._ictr = 0
    #     return iter(self._data)

    def __len__(self):
        return len(self._data)

    # def __next__(self):
    #     self._ictr += 1
    #     if self._ictr == self._size:
    #         raise StopIteration
    #     return self._data[self._ictr]

    def __getitem__(self, index: int) -> float:
        size = len(self)
        if index >= 0 and size > 0:
            ctr = index % size
            return self._data[ctr]
        raise ValueError(f"Zero size {size} or negative index {index} passed")

    # def __add__(self, other):
    #     retval = Signal(profname=self.profname)
    #     for ctr in range(0, len(self)):
    #         retval.append(self[ctr] + other[ctr])
    #     return retval

    # def __mul__(self, other):
    #     retval = Signal(profname=self.profname)
    #     for ctr in enumerate(self,0):
    #         retval.append(self[ctr] * other[ctr])
    #     return retval


class ToneGenerator:
    """Factory class for tone generators"""

    def __init__(self, profname: str = "default"):
        self._profname = profname
        (samp, bdep) = Profiles().content(self._profname)
        self._rate = samp
        self._depth = bdep

    def triangle(self):
        """Placeholder"""

    def sinusoid(self, freq: float, secs: float, offset: float = 0.0):
        """Sinusoid tone generator"""
        samples: int = round(self._rate * secs)
        delt: float = 1.0 / float(self._rate)
        for samp in range(0, samples):
            tim: float = delt * float(samp)
            val: float = sin((freq * 2.0 * pi * tim) + offset)
            yield val
