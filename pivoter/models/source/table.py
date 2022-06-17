"""
Classes representing a single cell of data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .cell import Cell
from pivoter.exceptions import UnnamedTableError


class Table:
    """
    Represents a table of data in the from of a list of cells.
    """

    def __init__(self, cells: Optional[List[Cell]] = None):
        self.cells = cells

    def add_cell(self, cell: Cell):
        if not self.cells:
            self.cells = []
        self.cells.append(cell)


@dataclass
class LiveTable:
    """
    A "live" table represents two things:

    1.) "printine" - The pristine table as pulled from the source.
    2.) "filtered" - The current subset of cells as selected from the pristine table.

    Keeping track of the pristine cell selection (the initial table) allows us to
    extend a Table of cells (.filtered) via comparing it with the pristine Table
    (.pristine). This enables the extension of a cell selection as well as the
    filtering down of one.
    """

    pristine: Table
    filtered: Table
    _name: str

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
    def name(self, name: Optional[str] = None):
        if name:
            self._name = name
        else:
            self._name = None

    @staticmethod
    def from_table(table: Table, name: str = None) -> LiveTable:
        """
        Given a table and optional it's name, create a livetable.
        """
        return LiveTable(_name=name, pristine=table, filtered=table)

    def _table_lengths_match(self):
        """
        Assert lengths of the pristine and filtered tables
        match. Principally for testing.
        """
        return len(self.pristine.cells) == len(self.filtered.cells)
