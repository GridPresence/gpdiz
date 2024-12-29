# -*- coding: utf-8 -*-
"""
App for library-level CLI calls
"""
import os
import time
from pathlib import Path
from typing import List, Dict
from typing_extensions import Annotated

import typer


app = typer.Typer()


# pylint: disable=too-many-instance-attributes
class SudCell:
    """Class dox"""

    def __init__(self, row: int, col: int, val: int = 0, dim: int = 3):
        self._row: int = row
        row_div: int = self._row // dim
        self._col: int = col
        col_div: int = self._col // dim
        self._block: int = (dim * row_div) + col_div

        self._poss: List[int] = []
        self._val = val
        if self._val == 0:
            self._solved: bool = False
            for x in range(1, 10):
                self._poss.append(x)
        else:
            self._solved = True

    def eliminate(self, val: int) -> bool:
        """Remove a value from the list of possibles"""
        retval: bool = False
        if val in self._poss:
            self._poss.remove(val)
            retval = True
        return retval

    def poss_str(self) -> str:
        """Debugging aid"""
        retval = "["
        for item in self._poss:
            retval = f"{retval} {str(item)}"
        retval = f"{retval} ]"
        return retval

    @property
    def row(self):
        """Accessor"""
        return self._row

    @property
    def col(self):
        """Accessor"""
        return self._col

    @property
    def block(self):
        """Accessor"""
        return self._block

    @property
    def solved(self):
        """Accessor"""
        return self._solved

    @solved.setter
    def solved(self, value: bool):
        self._solved = value

    @property
    def val(self):
        """Accessor"""
        return self._val

    @val.setter
    def val(self, value: int):
        self._val = value
        self._solved = True
        self._poss = []

    @property
    def poss(self):
        """Accessor"""
        return self._poss

    def reconciles(self) -> bool:
        """
        Check if this cell can be reconciled to a single value
        and thus solved
        """
        retval = False
        if len(self._poss) == 1:
            self._val = self._poss[0]
            self._poss.remove(self._val)
            self._solved = True
            retval = True
        return retval


class Sudoku:
    """Class dox"""

    def __init__(self, src: Path):
        self._dim = 3
        self._len = self._dim * self._dim
        self._cells: List[SudCell] = []
        self._updated: bool = False
        self._initialise(src)

    def _initialise(self, source: Path):
        with open(source, mode="r", encoding="utf8") as src:
            text: List[str] = src.read().splitlines()
        rowctr = 0
        for txtrow in text:
            for colctr in range(self._len):
                nval = int(txtrow[colctr])
                self._cells.append(SudCell(row=rowctr, col=colctr, val=nval))
            rowctr = rowctr + 1

    def set(self, index: int, axis: str) -> List[SudCell]:
        """Pulls a set of SudCells as a row, column or block"""
        retval: List[SudCell] = []
        if axis in ["row", "col", "block"]:
            match (axis):
                case "row":
                    for item in self._cells:
                        if item.row == index:
                            retval.append(item)
                case "col":
                    for item in self._cells:
                        if item.col == index:
                            retval.append(item)
                case "block":
                    for item in self._cells:
                        if item.block == index:
                            retval.append(item)
        else:
            raise ValueError(f"Unsupported axis specification: {axis}")
        return retval

    def _rowstr(self, row: int) -> str:
        sample: List[SudCell] = self.set(row, "row")
        retval: str = ""
        for col in range(self._len):
            for item in sample:
                if item.col == col:
                    if item.val == 0:
                        chur = " . "
                    else:
                        chur = f" {str(item.val)} "
                    retval = f"{retval}{chur}"
        return retval

    def __str__(self) -> str:
        retval: str = ""
        for row in range(self._len):
            retval = f"{retval}\n{self._rowstr(row)}"
        retval = f"{retval}\n"
        return retval

    # pylint: disable=too-many-branches
    def analyse(self, coll: List[SudCell]):
        """Check a set of cells for eliminations"""
        vals: List[int] = []
        all_possibles: List[int] = []
        freqs: Dict[int, int] = {}

        for item in coll:
            if item.solved is True:
                vals.append(item.val)
            else:
                all_possibles.extend(item.poss)
        for ind in all_possibles:
            if ind in freqs:
                freqs[ind] = freqs[ind] + 1
            else:
                freqs[ind] = 1
        for v in vals:
            for item in coll:
                if item.solved is False:
                    suxs = item.eliminate(v)
                    if suxs is True:
                        self._updated = suxs
        for item in coll:
            if item.solved is False:
                for cand in item.poss:
                    if freqs[cand] == 1:
                        item.val = cand
                        self._updated = True

    def reconcile(self):
        """Check whether values can be updated and possibles cleared"""
        for item in self._cells:
            if item.reconciles():
                self._updated = True

    def iterate(self):
        """Run an iteration across the puzzle to check for obvious
        eliminations from the list of possibles"""
        self._updated = False
        for r in range(self._len):
            ss = self.set(r, "row")
            self.analyse(ss)
        for c in range(self._len):
            ss = self.set(c, "col")
            self.analyse(ss)
        for b in range(self._len):
            ss = self.set(b, "block")
            self.analyse(ss)
        self.reconcile()
        os.system("clear")
        print(f"\n{str(self)}\n")
        time.sleep(1)

    def resolve(self):
        """Try and solve the puzzle"""
        os.system("clear")
        print(f"\n{str(self)}\n")
        time.sleep(1)
        self.iterate()
        while self._updated is True:
            self.iterate()

    def deconstruct(self):
        """Debugging analysis for incomplete puzzles"""
        for item in self._cells:
            if item.solved is False:
                print(
                    f"{item.row}, {item.col}, {item.block}: {item.val} {item.poss_str()}"
                )


@app.command()
def solve(
    name: Annotated[str, typer.Argument(help="Puzzle definition file name")],
) -> None:
    """
    Command for solving the puzzle.
    """
    puzzle_path: Path = Path(name).resolve()
    puzzle: Sudoku = Sudoku(puzzle_path)
    start = str(puzzle)
    puzzle.resolve()
    print("\n\n")
    print(start)
    print("\n\n")
    print(str(puzzle))
    puzzle.deconstruct()
