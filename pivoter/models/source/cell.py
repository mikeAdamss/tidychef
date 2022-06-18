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

    def is_above(self, cell: BaseCell) -> bool:
        """
        When compared to another cell, is this
        cell above it?
        """
        return self.y < cell.y

    def is_below(self, cell: BaseCell) -> bool:
        """
        When compared to another cell, is this
        cell below it?
        """
        return self.y > cell.y

    def is_right_of(self, cell: BaseCell) -> bool:
        """
        When compared to another cell, is this
        cell to the right of it?
        """
        return self.x > cell.x

    def is_left_of(self, cell: BaseCell) -> bool:
        """
        When compared to another cell, is this
        cell to the left of it?
        """
        return self.x < cell.x


@dataclass
class Cell(BaseCell):
    """
    Denotes a cell of data from a tabulated data source
    """

    value: Optional[str]

    # Optional as some tabullated formats (eg csv) do not have
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

    def _as_xy_str(self) -> str:
        """
        Returns a str representation of the current cell
        with xy co-ordinates and value.
        """
        return f"x:{self.x}, y:{self.y}, value = {self.value}"
