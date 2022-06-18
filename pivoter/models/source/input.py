"""
Classes representing a single input.

An input would be a single tabulated source. Csv, Excel, ODF or the in memory
representation of same (to include dataframes).
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from .table import LiveTable
from pivoter.configuration import ConfigController
from pivoter.exceptions import IllegalOperationError, IteratingSingleTableError
from pivoter.models.source.cell import BaseCell, Cell
from pivoter.selection import datamethods


class BaseInput:
    """
    A class representing a single input (typically though not exclusively a file).

    BaseInput will never be instantiated in its own right. But instead will inform
    pivoter.selection.base.Selectable and its children.
    """

    def __init__(
        self,
        is_singleton_table: bool,
        selected_table: LiveTable,
        cfg: ConfigController = ConfigController.from_ini(),
        had_initial_path: Path = None,
        tables: List[LiveTable] = None,
    ):
        self.cfg = cfg
        self.is_singleton_table = is_singleton_table
        self.selected_table = selected_table
        self.had_initial_path = had_initial_path
        self.tables = tables
        self.datamethods = datamethods.DataMethods

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

    @property
    def cells(self) -> List[Cell]:
        """
        Accessor for currently selected cells from the
        currently selected table
        """
        return self.selected_table.filtered.cells

    @cells.setter
    def cells(self, cells: List[Cell]):
        """
        Setter for the cells property
        """
        self.selected_table.filtered.cells = cells

    @property
    def pcells(self) -> List[BaseCell]:
        """
        Accessor for the pristine cells from the
        currently selected table
        """
        return self.selected_table.pristine.cells

    @pcells.setter
    def pcells(self, cells: List[BaseCell]):
        """
        Illegal method. This is defensive programming and
        will raise an error. There are no circumatances
        where you should ever modify you pristine record
        of the source data.

        If you are attempting to do this, you are trying to
        achieve something that is fundementally wrong.
        """
        raise IllegalOperationError(
            "You should never, under any circumstances be attempting to modify the pristne record of which cells were ingested for this table."
        )

    def __iter__(self):
        """
        We're not really iterating table objects, we're just moving the
        pointer to the selected table then returning the updated self
        """
        if self.is_singleton_table:
            raise IteratingSingleTableError

        for table in self.tables:
            self.selected_table = table
            yield self
