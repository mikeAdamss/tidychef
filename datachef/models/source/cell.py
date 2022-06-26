"""
Classes representing a sinlge cell of data.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import CellType
from typing import Optional

from datachef.exceptions import InvalidCellObjectError

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

    def is_above(self, y: int) -> bool:
        """
        When compared to a y index, is this
        cell above it?
        """
        return self.y < y

    def is_below(self, y: int) -> bool:
        """
        When compared to a y index, is this
        cell below it?
        """
        return self.y > y

    def is_right_of(self, x: int) -> bool:
        """
        When compared to an x index, is this
        cell to the right of it?
        """
        return self.x > x

    def is_left_of(self, x: int) -> bool:
        """
        When compared to an x index, is this
        cell to the left of it?
        """
        return self.x < x


@dataclass
class Cell(BaseCell):
    """
    Denotes a cell of data from a tabulated data source
    """

    value: Optional[str]

    # Optional as some tabullated formats (eg csv) do not have
    # cell formatting.
    cellformat: Optional[CellFormatting] = None

    def is_blank(self, disregard_whitespace: bool = True):
        """
        Can the contents of the cell be regarded as blank
        """
        if isinstance(self.value, str):
            v = self.value.strip() if disregard_whitespace else self.value
            if v == "":
                return True
            else:
                return False
        elif not self.value:
            return True
        else:
            raise InvalidCellObjectError(
                f"Error with {self._as_xy_str()} A cell should have a str or nan/None value"
            )

    def is_not_blank(self, disregard_whitespace: bool = True):
        """
        Can the contents of the cell be regarded as not blank
        """
        return not self.is_blank(disregard_whitespace=disregard_whitespace)

    def _as_xy_str(self) -> str:
        """
        Returns a str representation of the current cell
        with xy co-ordinates and value.
        """
        return f'x:{self.x}, y:{self.y}, value = "{self.value}"'