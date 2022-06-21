import copy
from typing import List, FrozenSet, Tuple, Optional, Union

from pivoter.exceptions import BadShiftParameterError, LoneValueOnMultipleCellsError, OutOfBoundsError
from pivoter.models.source.cell import BaseCell, Cell
from pivoter.models.source.input import BaseInput
from pivoter.cardinal.directions import UP, DOWN, LEFT, RIGHT, BaseDirection
from pivoter.selection import datafuncs as dfc

class Selectable(BaseInput):
    """
    Selection methods that are generic to all tabulated source inputs.
    """

    def assert_one(self):
        """
        Assert that the current selection contains exactly one cell
        """
        assert len(self.cells) == 1, f'Selection contains {len(self.cells)} cells, not 1'

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
        self.cells = [x for x in self.cells if x.is_blank(disregard_whitespace)]

    def is_not_blank(self, disregard_whitespace=True):
        """
        Filters the selection to those cells that are not blank.

        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the disregard_whitespace keyword.
        """
        self.cells = [x for x in self.cells if x.is_not_blank(disregard_whitespace)]

    def expand(self, direction: Tuple[int, int]):
        """
        Given a direction of UP, DOWN, LEFT, RIGHT
        Expands the current selection of cells in that direction.

        Notes:
        - Will also accept ABOVE and BELOW as direction, as they
        are aliases of UP and DOWN respectively.
        """

        potential_cells: List[Cell] = dfc.cells_not_in(
            self.cells, self.pcells
        )

        selection: List[BaseCell] = []
        if direction in [UP, DOWN]:  # so also ABOVE and BELOW

            all_used_x_indicies: FrozenSet[int] = set(c.x for c in self.cells)
            for xi in all_used_x_indicies:
                selected_cells_on_xi = dfc.cells_on_x_index(
                    self.cells, xi
                )

                potential_cells_on_xi: List[Cell] = [
                    c for c in potential_cells if c.x == xi
                ]

                if direction == UP:
                    highest_selected_cell_on_xi = (
                        dfc.minium_y_offset_cell(selected_cells_on_xi)
                    )
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_above(highest_selected_cell_on_xi)
                    ]

                if direction == DOWN:
                    lowest_selected_cell_on_xi = (
                        dfc.maximum_y_offset_cell(selected_cells_on_xi)
                    )
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_below(lowest_selected_cell_on_xi)
                    ]

        if direction in [LEFT, RIGHT]:

            all_used_y_indicies: FrozenSet[int] = set(c.y for c in self.cells)
            for yi in all_used_y_indicies:
                selected_cells_on_yi = dfc.cells_on_y_index(
                    self.cells, yi
                )

                potential_cells_on_yi: List[Cell] = [
                    c for c in potential_cells if c.y == yi
                ]

                if direction == LEFT:
                    leftmost_selected_cell_on_yi = (
                        dfc.minimum_x_offset_cell(selected_cells_on_yi)
                    )
                    selection += [
                        c
                        for c in potential_cells_on_yi
                        if c.is_left_of(leftmost_selected_cell_on_yi)
                    ]

                if direction == RIGHT:
                    rightmost_selected_cell_on_yi = (
                        dfc.maximum_x_offset_cell(selected_cells_on_yi)
                    )
                    selection += [
                        c
                        for c in potential_cells_on_yi
                        if c.is_right_of(rightmost_selected_cell_on_yi)
                    ]

        self.cells += selection
        return self

    def fill(self, direction: Tuple[int, int]):
        """
        Given a direction of UP, DOWN, LEFT, RIGHT
        Creates a new selection from the cells in that direction
        relative to the current cell selection.

        Notes:
        - Will also accept ABOVE and BELOW as direction, as they
        are aliases of UP and DOWN respectively.
        """
        did_have = copy.deepcopy(self.cells)
        self = self.expand(direction)
        self.cells = [x for x in self.cells if x not in did_have]
        return self

    def shift(self, direction_or_x: Union[BaseDirection, int], possibly_y: Optional[int] = None):
        """
        Move the entire selection relatively based on the changes
        to x and/or y coordinates received.
        """

        if isinstance(direction_or_x, int):
            if not isinstance(possibly_y, int):
                raise BadShiftParameterError()
            x = direction_or_x
            y = possibly_y
        elif isinstance(direction_or_x, BaseDirection):
            assert not possibly_y, 'Where passing a direction into shift, that must be the only argument'
            x = direction_or_x.x
            y = direction_or_x.y
        else:
            raise BadShiftParameterError()

        wanted_cells: List[BaseCell] = [BaseCell(x=c.x+x, y=c.y+y) for c in self.cells]

        found_cells = dfc.matching_xy_cells(self.pcells, wanted_cells)

        if len(dfc.cells_not_in(self.pcells, found_cells)) > 0:
            raise OutOfBoundsError()

        self.cells = found_cells
        return self