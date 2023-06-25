"""
Classes representing a sinlge cell of data.
"""
from __future__ import annotations

from dataclasses import dataclass
from os import linesep
from typing import Optional

from datachef.exceptions import (
    InvalidCellObjectError,
    InvlaidCellPositionError,
    NonExistentCellComparissonError,
)
from datachef.utils import cellutils

from .cellformat import CellFormatting


@dataclass
class BaseCell:
    """
    A primitive non value holding cell construct.
    """

    x: Optional[int] = None
    y: Optional[int] = None

    def _confirm_not_virtual(self):
        """
        Confirms that a cell is not virtual and that
        the user us not attempting positional comparissons
        between an existent and non existent cell entity
        """
        if self.x is None or self.y is None:
            raise NonExistentCellComparissonError(
                "You cannot reference or use for comparison the "
                "positional information of a virtual cell as it "
                "does not exist in the source data, i.e it has no "
                f"position information.{linesep}"
                f'The value of the cell in question is "{self.value}"'
            )

    def matches_xy(self, other_cell: BaseCell):
        """
        Does this objects x and y attributes, match
        the x and y attributes of the provided BaseCell or Cell
        object.
        """
        self._confirm_not_virtual()
        return self.x == other_cell.x and self.y == other_cell.y

    def is_above(self, y: int) -> bool:
        """
        When compared to a y index, is this
        cell above it?

        We mean "above" in visual terms, i.e
        does it have a lower vertical offset
        from the top of the table.
        """
        self._confirm_not_virtual()
        return self.y < y

    def is_below(self, y: int) -> bool:
        """
        When compared to a y index, is this
        cell below it?

        We mean "below" in visual terms, i.e
        does it have a higher vertical offset
        from the top of the table.
        """
        self._confirm_not_virtual()
        return self.y > y

    def is_right_of(self, x: int) -> bool:
        """
        When compared to an x index, is this
        cell to the right of it?
        """
        self._confirm_not_virtual()
        return self.x > x

    def is_left_of(self, x: int) -> bool:
        """
        When compared to an x index, is this
        cell to the left of it?
        """
        self._confirm_not_virtual()
        return self.x < x

    def _excel_ref(self) -> str:
        """
        Get the excel reference of the cell
        """

        x_ref = cellutils.x_to_letters(self.x) if self.x is not None else self.x
        y_ref = cellutils.y_to_number(self.y) if self.y is not None else self.y

        if any([x_ref and not y_ref, y_ref and not x_ref]):
            raise InvlaidCellPositionError(
                "Every cell object must have both an x and y position or neither."
                f"Got cell with x: {self.x} and y: {self.y}"
            )

        if x_ref and y_ref:
            return f"{x_ref}{y_ref}"
        return "VIRTUAL CELL"


@dataclass
class VirtualCell(BaseCell):
    """
    Where we are establishing relationships between a concrete cell
    from the tabulated data source and a constant or external value
    we do so via a virtual cell.

    VirtualCells are unique amongst cell variants in that they can
    have None positional values for x and y.
    """

    value: Optional[str] = None
    x: Optional[str] = None
    y: Optional[str] = None

    def __repr__(self):
        """
        Create a representation of this virtual cell in the form:
        <VIRTUAL CELL: value>
        """
        return f'<{self._excel_ref()}, value:"{self.value}">'


@dataclass
class Cell(BaseCell):
    """
    Denotes a cell of data from a tabulated data source
    """

    value: Optional[str] = None
    x: Optional[str] = None
    y: Optional[str] = None

    # Optional as some tabulated formats (eg csv) do not have
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

        if not self.value:
            return True

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

    def __repr__(self):
        """
        Create a representation of this cell in the form:
        <excel ref: value>

        eg:
        <A1, value:"value of a1", x:{x}, y:{y}>
        """
        return f'<{self._excel_ref()}, value:"{self.value}", x:{self.x}, y:{self.y}>'

    def __str__(self):
        """
        Create a representation of this cell in the form:
        <excel ref: value>

        eg:
        <A1, value:"value of a1", x:{x}, y:{y}>
        """
        return self.__repr__()
