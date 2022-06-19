import copy
from typing import List, FrozenSet, Tuple

from pivoter.exceptions import LoneValueOnMultipleCellsError
from pivoter.models.source.cell import BaseCell, Cell
from pivoter.models.source.input import BaseInput
from pivoter.constants import UP, DOWN, LEFT, RIGHT


class Selectable(BaseInput):
    """
    Selection methods that are generic to all tabulated source inputs.
    """

    def lone_value(self) -> str:
        """
        Confirms the selection contains exactly one cell, then returns
        the value of that cell
        """
        if len(self.cells) != 1:
            raise LoneValueOnMultipleCellsError(len(self.cells))
        return self.cells[0].value

    def is_blank(self, discount_whitespace=True):
        """
        Filters the selection to those cells that are blank.

        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the discount_whitespace keyword.
        """
        self.cells = [x for x in self.cells if x.is_blank(discount_whitespace)]

    def is_not_blank(self, discount_whitespace=True):
        """
        Filters the selection to those cells that are not blank.

        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the discount_whitespace keyword.
        """
        self.cells = [x for x in self.cells if x.is_not_blank(discount_whitespace)]

    def expand(self, direction: Tuple[int, int]):
        """
        Given a direction of UP, DOWN, LEFT, RIGHT
        Expands the current selection of cells in that direction.

        Notes:
        - Will also accept ABOVE and BELOW as direction, as they
        are aliases of UP and DOWN respectively.
        """

        potential_cells: List[Cell] = self.datamethods._cells_not_in(
            self.cells, self.pcells
        )

        selection: List[BaseCell] = []
        if direction in [UP, DOWN]:  # so also ABOVE and BELOW

            all_used_x_indicies: FrozenSet[int] = set(c.x for c in self.cells)
            for xi in all_used_x_indicies:
                selected_cells_on_xi = [c for c in self.cells if c.x == xi]

                potential_cells_on_xi: List[Cell] = [
                    c for c in potential_cells if c.x == xi
                ]

                if direction == UP:
                    highest_selected_cell_on_xi = (
                        self.datamethods._minium_y_offset_cell(selected_cells_on_xi)
                    )
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_above(highest_selected_cell_on_xi)
                    ]

                if direction == DOWN:
                    lowest_selected_cell_on_xi = (
                        self.datamethods._maximum_y_offset_cell(selected_cells_on_xi)
                    )
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_below(lowest_selected_cell_on_xi)
                    ]

        if direction in [LEFT, RIGHT]:

            all_used_y_indicies: FrozenSet[int] = set(c.y for c in self.cells)
            for yi in all_used_y_indicies:
                selected_cells_on_yi = [c for c in self.cells if c.y == yi]

                potential_cells_on_yi: List[Cell] = [
                    c for c in potential_cells if c.y == yi
                ]

                if direction == LEFT:
                    leftmost_selected_cell_on_yi = (
                        self.datamethods._minimum_x_offset_cell(selected_cells_on_yi)
                    )
                    selection += [
                        c
                        for c in potential_cells_on_yi
                        if c.is_left_of(leftmost_selected_cell_on_yi)
                    ]

                if direction == RIGHT:
                    rightmost_selected_cell_on_yi = (
                        self.datamethods._maximum_x_offset_cell(selected_cells_on_yi)
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
