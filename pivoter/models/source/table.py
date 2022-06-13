"""
Classes representing a single cell of data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .cell import BaseCell,Cell
import pivoter.exceptions
from pivoter.utils import cellutils
from pivoter.exceptions.common import OutOfBoundsError

class Table:
    def __init__(self, cells: Optional[List[Cell]] = None):
        self.cells = cells

    def add_cell(self, cell: Cell):
        if not self.cells:
            self.cells = []
        self.cells.append(cell)

    def _filtered_xy_match(self, wanted_basecells: List[BaseCell]):
        """
        Given a list of BaseCell's. Filter .cells down to those
        that match the required x & y attributes.

        Raise where a requested cell does not exist. 
        """

        ecell: Cell # existing cell
        wcell: BaseCell # wanted cell

        found_cells = [
            ecell for ecell in self.cells if any(
                [ecell.matches_xy(wcell) for wcell in wanted_basecells]
                )
            ]

        if len(found_cells) != len(wanted_basecells):
            unfound_cells = [
            wcell for wcell in self.cells if not any(
                [wcell.matches_xy(ecell) for ecell in wanted_basecells]
                )
            ]

            unfound_cells_as_excel = [cellutils.basecells_to_excel_refs(x) for x in unfound_cells]
            raise OutOfBoundsError(f'These cells don\'t exist in the current selection: {unfound_cells_as_excel}')
        
        self.cells = found_cells

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
