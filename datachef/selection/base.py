import copy
import logging
from pathlib import Path
from typing import FrozenSet, List, Optional, Tuple, Union

from datachef.cardinal.directions import DOWN, LEFT, RIGHT, UP, BaseDirection
from datachef.exceptions import (
    BadShiftParameterError,
    LoneValueOnMultipleCellsError,
    OutOfBoundsError,
)
from datachef.models.source.cell import BaseCell, Cell
from datachef.models.source.input import BaseInput
from datachef.selection import datafuncs as dfc


class Selectable(BaseInput):
    """
    Inherits from BaseInput to add the following selection methods that are generic to all tabulated source inputs.
    """

    def assert_one(self):
        """
        Assert that the current selection contains exactly one cell
        """
        assert (
            len(self.cells) == 1
        ), f"Selection contains {len(self.cells)} cells, not 1"

    def lone_value(self) -> str:
        """
        Confirms the selection contains exactly one cell, then returns
        the value of that cell
        """
        if len(self.cells) != 1:
            raise LoneValueOnMultipleCellsError(len(self.cells))
        return self.cells[0].value

    def is_blank(self, disregard_whitespace=True):
        """
        Filters the selection to those cells that are blank.
        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the disregard_whitespace keyword.
        """
        return_self = copy.deepcopy(self)
        return_self.cells = [x for x in self.cells if x.is_blank(disregard_whitespace)]
        return return_self

    def is_not_blank(self, disregard_whitespace=True):
        """
        Filters the selection to those cells that are not blank.
        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the disregard_whitespace keyword.
        """
        self.cells = [x for x in self.cells if x.is_not_blank(disregard_whitespace)]

    def expand(self, direction: BaseDirection):
        """
        Given a direction of UP, DOWN, LEFT, RIGHT
        Expands the current selection of cells in that direction.

        Notes:
        - Will also accept ABOVE and BELOW as direction, as they
        are aliases of UP and DOWN respectively.
        """

        potential_cells: List[Cell] = dfc.cells_not_in(self.pcells, self.cells)

        selection: List[BaseCell] = []
        if direction in [UP, DOWN]:  # so also ABOVE and BELOW

            all_used_x_indicies: FrozenSet[int] = set(c.x for c in self.cells)
            for xi in all_used_x_indicies:
                selected_cells_on_xi = dfc.cells_on_x_index(self.cells, xi)

                potential_cells_on_xi: List[Cell] = [
                    c for c in potential_cells if c.x == xi
                ]

                if direction == UP:
                    uppermost_used_yi = dfc.minimum_y_offset(selected_cells_on_xi)
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_above(uppermost_used_yi)
                    ]

                if direction == DOWN:
                    lowest_used_xi = dfc.maximum_y_offset(selected_cells_on_xi)
                    selection += [
                        c for c in potential_cells_on_xi if c.is_below(lowest_used_xi)
                    ]

        if direction in [LEFT, RIGHT]:

            # For every row in which have at least one cell selected
            all_used_y_indicies: FrozenSet[int] = set(c.y for c in self.cells)
            for yi in all_used_y_indicies:

                # Get all currently selected cells on that row
                selected_cells_on_yi = dfc.cells_on_y_index(self.cells, yi)

                # Get all not selected cells on that row
                potential_cells_on_yi: List[Cell] = [
                    c for c in potential_cells if c.y == yi
                ]

                if direction == LEFT:

                    # Select anything to the left of the
                    # rightmost of the selected cells on this row
                    leftmost_used_yi = dfc.minimum_x_offset(selected_cells_on_yi)
                    selection += [
                        c
                        for c in potential_cells_on_yi
                        if c.is_left_of(leftmost_used_yi)
                    ]

                if direction == RIGHT:
                    rightmost_used_yi = dfc.maximum_x_offset(selected_cells_on_yi)
                    selection += [
                        c
                        for c in potential_cells_on_yi
                        if c.is_right_of(rightmost_used_yi)
                    ]

        return_self = copy.deepcopy(self)
        return_self.cells += selection
        return return_self

    def fill(self, direction: BaseDirection):
        """
        Creates a new selection from the cells in that direction
        relative to the current cell selection.

        :direction: One of UP, DOWN, LEFT, RIGHT
        """
        did_have = copy.deepcopy(self.cells)
        self = self.expand(direction)
        self.cells = [x for x in self.cells if x not in did_have]
        return self

    def shift(
        self,
        direction_or_x: Union[BaseDirection, int],
        possibly_y: Optional[int] = None,
    ):
        """
        Move the entire current selection relatively. Accepts a direction
        or raw x and y co-ordinates, examples:

        - .shift(RIGHT)
        - .shift(RIGHT(5))
        - .shift(2, 6)
        - .shift(-1, 4)
        """

        if isinstance(direction_or_x, int):
            if not isinstance(possibly_y, int):
                raise BadShiftParameterError()
            x = direction_or_x
            y = possibly_y
        elif isinstance(direction_or_x, BaseDirection):
            assert (
                not possibly_y
            ), "Where passing a direction into shift, that must be the only argument"
            x = direction_or_x.x
            y = direction_or_x.y
        else:
            raise BadShiftParameterError()

        wanted_cells: List[BaseCell] = [
            BaseCell(x=c.x + x, y=c.y + y) for c in self.cells
        ]

        found_cells = dfc.matching_xy_cells(self.pcells, wanted_cells)

        if len(found_cells) == 0 and len(wanted_cells) > 0:
            raise OutOfBoundsError()

        return_self = copy.deepcopy(self)
        return_self.cells = found_cells
        return return_self

    def excel_ref(self, excel_ref: str):
        """
        Selects just the cells as indicated by the provided excel style
        reference: "A6", "B17:B24": etc.
        """

        if ":" in excel_ref:
            wanted: List[BaseCell] = dfc.multi_excel_ref_to_basecells(excel_ref)
        else:
            wanted: BaseCell = dfc.single_excel_ref_to_basecell(excel_ref)
            wanted = [wanted]

        selected = dfc.exactly_matched_xy_cells(self.cells, wanted)

        return_self = copy.deepcopy(self)
        return_self.cells = selected
        return return_self
