"""
Classes representing a single input.

An input would be a single tabulated source. Csv, Excel, ODF or the in memory
representation of same (to include dataframes).
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Optional, List

from .cell import BaseCell
from .table import LiveTable, Table
from pivoter.exceptions import IteratingSingleTableError, LoneValueOnMultipleCellsError
from pivoter.utils import cellutils


def _input_from_single_table(file_path: Path, table: Table) -> Input:
    """
    Construct an Input object from a single table
    """
    return Input(
        is_singelton_table=True,
        selected_table=LiveTable.from_table(name=file_path.name, table=table),
        had_initial_path=file_path,
        tables=None,
    )


@dataclass
class Input:
    """
    A class representing a single input (typically though not exclusively a file)
    """

    is_singelton_table: bool
    selected_table: LiveTable

    had_initial_path: Optional[Path]
    tables: Optional[List[LiveTable]]


    @property
    def name(self) -> str:
        """
        Get name of currently selected table
        """
        return self.selected_table.name


    @property
    def title(self) -> str:
        """
        Alternate call to name.
        """
        return self.name


    def __iter__(self):
        if self.is_singelton_table:
            raise IteratingSingleTableError

        for table in self.tables:
            self.selected_table = table
            yield self

    """
    Dev notes:

    - At any given time the user will be utilising a single LiveTable.
    - A class:LiveTable consist of two class:Table's as follow:
        - pristine: all the cells the table had when loaded in, this is never modified.
        - filtered: the users current selection
    
    The following methods allow for iteration methods that will seem natural to the user
    The following methods all do one of two things:
    1.) Expand the current selection by comparing ".filtered" to ".pristine".
    2.) Filter down ".filtered" to a smaller selection.
    """

    def excel_ref(self, excel_ref: str):
        """
        Use an excel style reference to filter down the current selection of cells.

        An error will be raised if you ask for a cell that is not within the selection.
        """
        wanted_cells: List[BaseCell] = cellutils.get_ref_as_wanted_basecells(excel_ref)
        self.selected_table.filtered._filter_to_matching_xys(wanted_cells)
        return self


    def lone_value(self) -> str:
        """
        Where a selection has exactly one cell, return the value of that cell
        """
        if len(self.selected_table.filtered.cells) != 1:
            raise LoneValueOnMultipleCellsError(len(self.selected_table.filtered.cells))
        return self.selected_table.filtered.cells[0].value
