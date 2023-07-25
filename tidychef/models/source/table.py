"""
Classes representing a single cell of data.
"""

from __future__ import annotations

import copy
import uuid
from pathlib import Path
from typing import List, Optional, Union

import tidychef.datafuncs as dfc
from tidychef.exceptions import UnalignedTableOperation
from tidychef.models.source.cell import BaseCell, Cell
from tidychef.utils.decorators import dontmutate


class Table:
    """
    Represents a table of data in the form of a list of cell objects.
    """

    def __init__(self, cells: Optional[List[Cell]] = None):
        """
        Represents a table of data in the form of a list of cell objects.

        :param cells: A list of Cell objects representing the contents
        of a tabulated data source.
        """
        self.cells = None
        self._signature = str(uuid.uuid4())

    def add_cell(self, cell: Cell):
        if not self.cells:
            self.cells = []
        self.cells.append(cell)


class LiveTable:
    """
    A "live" table is the representation of a changing selection of cells as
    taken from a single tabulated input, it revolves around the control of
    two things:

    1.) "pristine" - The pristine table as pulled from the source.
    2.) "filtered" - The current subset of cells (up to all) as selected from the
                     pristine table.

    Keeping track of the pristine cell selection (the initial table) allows us to
    extend a Table of cells (.filtered) via comparing the two. This enables the
    easy extension of a cell selection as well as the filtering down of one.

    :param data_table: A tidychef Table object holding the cells representing
    a table.
    :param name: The name of the table where it has a name
    :param source: The filename, url or identifier of the source that has
    been ingested.
    """

    def __init__(self, data_table: Table, name: str = None, source: str = None):
        self.pristine: Table = data_table
        self.filtered: Table = copy.deepcopy(data_table)
        self._name: Optional[str] = name
        self.source: Optional[Union[Path, str]] = source

        # Label for a given selection
        self._label: Optional[str] = None

        # Cached
        self._maximum_pristine_x: Optional[int] = None
        self._minimum_pristine_x: Optional[int] = None
        self._maximum_pristine_y: Optional[int] = None
        self._minimum_pristine_y: Optional[int] = None

        # Config options
        self._explain: bool = False
        self._explain_path = None

    @property
    def maximum_pristine_x(self) -> int:
        """
        Get the minimum pristine y offset
        """
        if self._maximum_pristine_x is not None:
            return self._maximum_pristine_x
        else:
            self._maximum_pristine_x = dfc.maximum_x_offset(self.pcells)
            return self._maximum_pristine_x

    @property
    def minimum_pristine_x(self) -> int:
        """
        Get the minimum pristine y offset
        """
        if self._minimum_pristine_x is not None:
            return self._minimum_pristine_x
        else:
            self._minimum_pristine_x = dfc.minimum_x_offset(self.pcells)
            return self._minimum_pristine_x

    @property
    def maximum_pristine_y(self) -> int:
        """
        Get the minimum pristine y offset
        """
        if self._maximum_pristine_y is not None:
            return self._maximum_pristine_y
        else:
            self._maximum_pristine_y = dfc.maximum_y_offset(self.pcells)
            return self._maximum_pristine_y

    @property
    def minimum_pristine_y(self) -> int:
        """
        Get the minimum pristine y offset
        """
        if self._minimum_pristine_y is not None:
            return self._minimum_pristine_y
        else:
            self._minimum_pristine_y = dfc.minimum_y_offset(self.pcells)
            return self._minimum_pristine_y

    @property
    def label(self):
        """
        Accessor for current label of current selection of cells.
        """
        return self._label

    @dontmutate
    def label_as(self, label: str):
        """
        Assign a label to this specific selection

        :param label: The label we want to set.
        """
        assert isinstance(label, str), "A label for a selection must be of type string"
        self._label = label
        return self

    def __len__(self):
        return len(self.cells)

    @property
    def name(self):
        """
        Return a name if we have a name, else raises
        """
        if self._name:
            return self._name
        else:
            return "Unnamed Table"

    @property
    def cells(self) -> List[Cell]:
        """
        Accessor for currently selected cells from the
        currently selected table
        """
        return self.filtered.cells

    @cells.setter
    def cells(self, cells: List[Cell]):
        """
        Setter for the cells property

        :param cells: A lost of cells representing the
        currently selected cells from the table.
        """
        self.filtered.cells = cells

    @property
    def pcells(self) -> List[BaseCell]:
        """
        Accessor for the pristine cells from the
        currently selected table
        """
        return self.pristine.cells

    def selections_made(self) -> bool:
        """
        Have any selections been made
        """
        return len(self.pristine.cells) != len(self.filtered.cells)

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def signature(self) -> str:
        """
        A uuid that uniquely identifies a parsed input source table
        """
        return self.filtered._signature

    @dontmutate
    def __sub__(self, other_input: LiveTable):
        """
        Implements "-" operator, subtraction

        Allows subtraction of one selection from the same distinct
        and currently selected table from another. Provided they
        are derived from the same initial BaseInput.

        :param other_input: Another instance of this class
        whose selected cells we wish to subtract from the
        selected cells of this instance.
        """

        if self.signature != other_input.signature:
            raise UnalignedTableOperation(
                "Selections can only be combined or previewed in combination "
                "if they are taken from the exact same table as taken from a single "
                "instance of a parsed input."
            )

        cells = self.cells if self.selections_made() else self.pcells
        self.cells = dfc.cells_not_in(cells, other_input.cells)
        return self

    # TODO - type hint this
    @dontmutate
    def __or__(self, other_input: LiveTable):
        """
        Implements "|" operator, union.

        Allows the union of one selection from the same distinct
        and currently selected table with another. Provided they
        are derived from the same initial BaseInput.

        :param other_input: Another instance of this class
        whose cells we want to Union | with the cells of
        this class.
        """
        if self.signature != other_input.signature:
            raise UnalignedTableOperation(
                "Selections can only be combined or previewed in combination "
                "if they are taken from the exact same table as taken from a single "
                "instance of a parsed input."
            )

        new_cells = dfc.cells_not_in(other_input.cells, self.cells)
        self.cells = self.cells + new_cells
        return self

    # TODO - type hint this
    def __iter__(self):
        """ """
        for cell in self.cells:
            yield cell

    def __str__(self):
        return str(self.cells)
