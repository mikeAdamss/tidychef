"""
Classes representing a sinlge cell of data.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .cellformat import CellFormatting


@dataclass
class BaseCell:
    """
    A primitive non value holding cell construct.

    Used in two scenarios:
    - The base class for class:Cell
    - Denoting x,y offsets of cells requested. Queries
    compare BaseCell's with Cell's
    """

    x: int
    y: int

    def matches_xy(self, other_cell: BaseCell):
        """
        Does this objects x and y attributes, match
        the x and y attributes of the provided BaseCell or Cell
        object.
        """
        return self.x == other_cell.x and self.y == other_cell.y


@dataclass
class Cell(BaseCell):
    """
    Denotes a cell of data from a tabulated data source
    """

    value: Optional[str]

    # Optional as some tabllated formats (eg csv) do not have
    # cell formatting.
    cellformat: Optional[CellFormatting] = None

    @property
    def blank(self):
        """
        Can the contents of the cell be regarded as blank
        """
        if isinstance(self.value, str):
            if self.value.strip() == "":
                return True
        elif not self.value:
            return True
        else:
            return False
