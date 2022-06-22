"""
Classes representing a single cell of data.
"""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass
from os import linesep
from typing import List, Optional

from pivoter.exceptions import InvalidTableSignatures, UnnamedTableError

from .cell import Cell


class Table:
    """
    Represents a table of data in the form of a list of cells.
    """

    def __init__(self, cells: Optional[List[Cell]] = None):
        self.cells = cells
        self._signature = str(uuid.uuid4())

    def add_cell(self, cell: Cell):
        if not self.cells:
            self.cells = []
        self.cells.append(cell)

    def _as_xy_str(self, demarcation=linesep) -> str:
        """
        Returns a str represtentation of the current cells
        with their xy co-ordinates and values.
        """
        mystr = ""
        for cell in self.cells:
            mystr += f"{cell._as_xy_str()}{demarcation}"
        return mystr.strip()


class LiveTable:
    """
    A "live" table represents two things:

    1.) "pristine" - The pristine table as pulled from the source.
    2.) "filtered" - The current subset of cells (up to all) as selected from the pristine table.

    Keeping track of the pristine cell selection (the initial table) allows us to
    extend a Table of cells (.filtered) via comparing it with the pristine Table
    (.pristine). This enables the extension of a cell selection as well as the
    filtering down of one.
    """

    def __init__(self, pristine: Table, filtered: Table, _name: str = None):
        self.pristine: Table = pristine
        self.filtered: Table = filtered
        self._name: Optional[str] = _name
        self.validate()

    @property
    def name(self):
        """
        Return a name if we have a name, else raises
        """
        if self._name:
            return self._name
        else:
            raise UnnamedTableError()

    @name.setter
    def name(self, name: str):
        self._name = name

    def validate(self):
        """
        Confirm class is validly constructed.
        """
        if self.pristine._signature != self.filtered._signature:
            raise InvalidTableSignatures()

    @staticmethod
    def from_table(table: Table, name: str = None) -> LiveTable:
        """
        Given a table and optional it's name, create a livetable.
        """
        return LiveTable(
            pristine=table,
            filtered=copy.deepcopy(table),
            _name=name,
        )
