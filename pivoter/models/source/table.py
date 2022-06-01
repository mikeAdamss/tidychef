"""
Classes representing a single cell of data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .cell import Cell
import pivoter.exceptions


class Table:

    def __init__(self, cells: Optional[List[Cell]] = None):
        self.cells = cells

    def add_cell(self, cell: Cell):
        if not self.cells:
            self.cells = []
        self.cells.append(cell)

    def _has_length(self, expected_len: int):
        """
        Compare length (number of cells) with expected length
        """
        return len(self.cells) == expected_len

 
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
    name: str

    @property
    def title(self):
        """
        Alternative accessor for table.name.
        Returns a name if we have a name, else raises
        """
        return self.name()

    @property
    def name(self):
        """
        Return a name if we have a name, else raises
        """
        if self._name:
            return self._name
        else:
            raise pivoter.exceptions.UnnamedTableError

    @name.setter
    def name(self, name: Optional[str] = None):
        if name:
            self._name = name
        else:
            self._name = None

    @staticmethod
    def from_table(name: str, table: Table) -> LiveTable:
        return LiveTable(name=name, pristine=table, filtered=table)

    def _table_lengths_match(self):
        """
        Assert lengths of the pristine and filtered tables
        match. Principally for testing.
        """
        return len(self.pristine.cells) == len(self.filtered.cells)
