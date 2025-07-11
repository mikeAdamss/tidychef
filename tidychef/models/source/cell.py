"""
Classes representing a sinlge cell of data.
"""
from __future__ import annotations

from dataclasses import dataclass
from os import linesep
from typing import Optional

from tidychef.exceptions import (
    InvalidCellObjectError,
    InvlaidCellPositionError,
    NonExistentCellComparissonError,
)
from tidychef.utils import cellutils

from .cellformat import CellFormatting


@dataclass
class BaseCell:
    """
    A primitive non value holding cell construct.

    :param x: Index on the horizontal axis
    :param y: Index on the vertical axis
    """

    x: int
    y: int

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

    def matches_xy(self, other_cell: BaseCell) -> bool:
        """
        Does this objects x and y attributes, match
        the x and y attributes of the provided BaseCell or Cell
        object.

        :param other_cell: A different tidychef BaseCell or
        inheritor of.
        :return: True of cells have same table location, else False
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

        :param y: Vertical cell index (row number) to
        compare to.
        :return: is this Cell above this y
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

        :param y: Vertical cell index (row number) to
        compare to.
        :return: is this Cell below this y
        """
        self._confirm_not_virtual()
        return self.y > y

    def is_right_of(self, x: int) -> bool:
        """
        When compared to an x index, is this
        cell to the right of it?

        :param x: Horizontal cell index (column number) to
        compare to.
        :return: is this Cell right of x
        """
        self._confirm_not_virtual()
        return self.x > x

    def is_left_of(self, x: int) -> bool:
        """
        When compared to an x index, is this
        cell to the left of it?

        :param x: Horizontal cell index (column number) to
        compare to.
        :return: is this Cell left of x
        """
        self._confirm_not_virtual()
        return self.x < x

    def _excel_ref(self) -> str:
        """
        Get the excel reference of the cell

        :return: A string representation of this object.
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

    @property
    def excel_row(self) -> int:
        """
        What is the row number of the row
        containing this cell in excel terms
        """
        return cellutils.y_to_number(self.y)

    @property
    def excel_column(self) -> str:
        """
        What is the excel style column
        letter(s) for the column containing
        this cell.
        """
        return cellutils.x_to_letters(self.x)


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
    x: Optional[int] = None
    y: Optional[int] = None

    def __repr__(self):
        """
        Create a representation of this virtual cell in the form:
        <VIRTUAL CELL: value>
        """
        return f'({self._excel_ref()}, value:"{self.value}")'


@dataclass
class Cell(BaseCell):
    """
    Denotes a cell of data from a tabulated data source

    :param value: The contents of the cell as a string
    :param x: Index on the horizontal axis
    :param y: Index on the vertical axis
    :param cellformat: Optional attribute to hold format
    specific cell attributes
    """

    value: str
    x: int
    y: int

    # Optional as some tabulated formats (eg csv) do not have
    # cell formatting.
    cellformat: Optional[CellFormatting] = None

    # Derivable things. Better to do it on load once than every
    # time we need it.
    numeric: bool = False

    def __post_init__(self):
        """
        We'll store the original value of the cell
        for where a cell value has been changed.
        """
        self._original_value = self.value
        
        # Derive if its numeric
        try:
            float(self.value)
            self.numeric = True
        except (ValueError, TypeError):
            pass


    def is_blank(self, disregard_whitespace: bool = True):
        """
        Can the contents of the cell be regarded as blank

        :param disregard_whitespace: Flag so we can choose to treat
        cells with just whitespace as populated.
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

        :param disregard_whitespace: Flag so we can choose to treat
        cells with just whitespace as populated.
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

        return f'({self._excel_ref()}, value:"{self.value}", x:{self.x}, y:{self.y})'
