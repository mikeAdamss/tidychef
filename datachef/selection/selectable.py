from __future__ import annotations

import copy
import re
from typing import FrozenSet, List, Optional, Union

from datachef.cardinal.directions import Direction, down, left, right, up
from datachef.exceptions import (BadExcelReferenceError,
                                BadShiftParameterError,
                                 LoneValueOnMultipleCellsError,
                                 OutOfBoundsError)
from datachef.models.source.cell import BaseCell, Cell
from datachef.models.source.table import LiveTable
from datachef.selection import datafuncs as dfc
from datachef.utils.decorators import dontmutate


class Selectable(LiveTable):
    """
    Inherits from LiveTable to add the following selection methods that are generic to all tabulated inputs.
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

    @dontmutate
    def is_blank(self, disregard_whitespace=True):
        """
        Filters the selection to those cells that are blank.
        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the disregard_whitespace keyword.
        """
        self.cells = [x for x in self.cells if x.is_blank(disregard_whitespace)]
        return self

    @dontmutate
    def is_not_blank(self, disregard_whitespace=True):
        """
        Filters the selection to those cells that are not blank.
        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the disregard_whitespace keyword.
        """
        self.cells = [x for x in self.cells if x.is_not_blank(disregard_whitespace)]
        return self

    @dontmutate
    def expand(self, direction: Direction):
        """
        Given a direction of UP, DOWN, LEFT, RIGHT
        Expands the current selection of cells in that direction.

        Notes:
        - Will also accept ABOVE and BELOW as direction, as they
        are aliases of UP and DOWN respectively.
        """

        potential_cells: List[Cell] = dfc.cells_not_in(self.pcells, self.cells)

        selection: List[BaseCell] = []
        if direction in [up, down]:  # so also above and below

            all_used_x_indicies: FrozenSet[int] = set(c.x for c in self.cells)
            for xi in all_used_x_indicies:
                selected_cells_on_xi = dfc.cells_on_x_index(self.cells, xi)

                potential_cells_on_xi: List[Cell] = [
                    c for c in potential_cells if c.x == xi
                ]

                if direction == up:
                    uppermost_used_yi = dfc.minimum_y_offset(selected_cells_on_xi)
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_above(uppermost_used_yi)
                    ]

                if direction == down:
                    lowest_used_xi = dfc.maximum_y_offset(selected_cells_on_xi)
                    selection += [
                        c for c in potential_cells_on_xi if c.is_below(lowest_used_xi)
                    ]

        if direction in [left, right]:

            # For every row in which have at least one cell selected
            all_used_y_indicies: FrozenSet[int] = set(c.y for c in self.cells)
            for yi in all_used_y_indicies:

                # Get all currently selected cells on that row
                selected_cells_on_yi = dfc.cells_on_y_index(self.cells, yi)

                # Get all not selected cells on that row
                potential_cells_on_yi: List[Cell] = [
                    c for c in potential_cells if c.y == yi
                ]

                if direction == left:

                    # Select anything to the left of the
                    # rightmost of the selected cells on this row
                    leftmost_used_yi = dfc.minimum_x_offset(selected_cells_on_yi)
                    selection += [
                        c
                        for c in potential_cells_on_yi
                        if c.is_left_of(leftmost_used_yi)
                    ]

                if direction == right:
                    rightmost_used_yi = dfc.maximum_x_offset(selected_cells_on_yi)
                    selection += [
                        c
                        for c in potential_cells_on_yi
                        if c.is_right_of(rightmost_used_yi)
                    ]

        self.cells += selection
        return self

    @dontmutate
    def fill(self, direction: Direction):
        """
        Creates a new selection from the cells in that direction
        relative to the current cell selection.

        :direction: One of: up, down, left, right
        """
        did_have = copy.deepcopy(self.cells)
        self = self.expand(direction)
        self.cells = [x for x in self.cells if x not in did_have]
        return self

    @dontmutate
    def shift(
        self,
        direction_or_x: Union[Direction, int],
        possibly_y: Optional[int] = None,
    ):
        """
        Move the entire current selection relatively. Accepts a direction
        or raw x and y co-ordinates, examples:

        - .shift(right)
        - .shift(right(5))
        - .shift(2, 6)
        - .shift(-1, 4)

        :param direction_or_x: Either a direction of the raw x offset
        of a direction.
        :param possibly_y: Either none or the raw y offset of a direciton
        """

        if isinstance(direction_or_x, int):
            if not isinstance(possibly_y, int):
                raise BadShiftParameterError()
            x_offset = direction_or_x
            y_offset = possibly_y
        elif isinstance(direction_or_x, Direction):
            assert (
                not possibly_y
            ), "Where passing a direction into shift, that must be the only argument"
            x_offset = direction_or_x.x
            y_offset = direction_or_x.y
        else:
            raise BadShiftParameterError()

        wanted_cells: List[BaseCell] = [
            BaseCell(x=c.x + x_offset, y=c.y + y_offset) for c in self.cells
        ]

        found_cells = dfc.matching_xy_cells(self.pcells, wanted_cells)

        if len(found_cells) == 0 and len(wanted_cells) > 0:
            raise OutOfBoundsError()

        self.cells = found_cells
        return self

    @dontmutate
    def excel_ref(self, excel_ref: str):
        """
        Selects just the cells as indicated by the provided excel style
        reference: "A6", "B17:B24", "9", "GH" etc.
        """

        # Multi excel reference:
        # eg: 'B2:F5'
        if re.match("^[A-Z]+[0-9]+:[A-Z]+[0-9]+$", excel_ref):
            wanted: List[BaseCell] = dfc.multi_excel_ref_to_basecells(excel_ref)
            selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
        
        # Single column and row reference
        # eg: 'F19'
        elif re.match("^[A-Z]+[0-9]+$", excel_ref):
            wanted: BaseCell = dfc.single_excel_ref_to_basecell(excel_ref)
            wanted = [wanted]
            selected = dfc.exactly_matched_xy_cells(self.cells, wanted)

        # An excel reference that is a single row number
        # eg: '4'
        elif re.match("^[0-9]+$", excel_ref):
            wanted_y_index: int = dfc.single_excel_row_to_y_index(excel_ref)
            selected = [c for c in self.cells if c.y == wanted_y_index]
        
        # An excel reference that is one of more column letter
        # eg: 'H'
        elif re.match("^[A-Z]+$", excel_ref):
            wanted_x_index: int = dfc.single_excel_column_to_x_index(excel_ref)
            selected = [c for c in self.cells if c.x == wanted_x_index]

        # Unknown excel reference
        else:
            raise BadExcelReferenceError(f'Unrecognised excel reference {excel_ref}')

        self.cells = selected
        return self

    @dontmutate
    def filter(self, check: callable):
        """
        Selects just the cells that match the provided check

        : param check: a function, lambda or callable class that
        returns a bool when given a single cell as a parameter.
        """

        self.cells = list(filter(check, self.cells))
        return self

    # Decorator unnecessary as we're calling another decorated method
    def re(self, pattern: str):
        """
        Filter the current selection of cells to only include
        cells whose value matches the provided regular expression
        pattern.
        """
        return self.filter(
            lambda cell: True if re.match(pattern, cell.value) else False
        )

    @dontmutate
    def spread(self, direction: Direction, until: Optional[Selectable] = None):
        """
        Spread a cell value into adjoining blank cells.

        If no offset is specified with the direction, then the
        spread will continue until terminated by the border of
        used cells or when it encounters a non blank cell.

        :param direction: A cardinal direction: up, down, left
        right with optional offset, i.e right(3)
        "param barrier" A selection of cells we do not want
        the spread to spread into 
        """

        if not isinstance(direction, Direction):
            raise ValueError(
                "Argument direction must be one of: up, down,"
                "left, right, above, below"
            )

        new_cells = []

        orderer = {
            "right": dfc.order_cells_leftright_topbottom,
            "left": dfc.order_cells_rightleft_bottomtop,
            "up": dfc.order_cells_bottomtop_rightleft,
            "above": dfc.order_cells_bottomtop_rightleft,
            "down": dfc.order_cells_topbottom_leftright,
            "below": dfc.order_cells_topbottom_leftright,

        }.get(direction.name)

        if not orderer:
            raise ValueError(
                'Unable to determine required cell consideration'
                f' order from direction: {direction}'
                )

        ordered_selected_cells: List[Cell] = orderer(self.cells)
        ordered_pristine_cells: List[Cell] = copy.deepcopy(orderer(self.pcells))

        selected_cell_index: int = 0
        considered_offset = None
        spreading = None
        for cell in ordered_pristine_cells:

            if considered_offset is None:
                considered_offset = cell.y if direction._horizontal_axis else cell.x
            elif considered_offset != (cell.y if direction._horizontal_axis else cell.x):
                spreading = None
                considered_offset = cell.y if direction._horizontal_axis else cell.x

            if not (selected_cell_index + 1) > len(ordered_selected_cells):
                if cell.matches_xy(ordered_selected_cells[selected_cell_index]):
                    spreading = cell.value
                    selected_cell_index += 1
                    continue

            if spreading is not None:
                if until:
                    if any(cell.matches_xy(c) for c in until.cells):
                        spreading = None
                        continue
                if cell.is_blank():
                    cell.value = spreading
                    new_cells.append(cell)
                else:
                    spreading = None

        # Remove cells we're overwriting
        self.cells = [
            c1 for c1 in self.cells if not any(c1.matches_xy(c2) for c2 in new_cells)
        ]

        # We also need to modify the pristine selection
        self.pristine.cells = [
            c1
            for c1 in self.pcells
            if not any(c1.matches_xy(c2) for c2 in new_cells)
        ]
        self.pristine.cells += new_cells

        # Add the overwritten cells into the current selection
        self.cells += new_cells
        return self
