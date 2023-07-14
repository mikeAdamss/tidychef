from __future__ import annotations

import copy
import re
from os import linesep
from typing import Callable, FrozenSet, List, Optional, Union

from datachef.against.implementations.base import BaseValidator
from datachef.direction.directions import (
    BaseDirection,
    Direction,
    above,
    below,
    down,
    left,
    right,
    up,
)
from datachef.exceptions import (
    BadExcelReferenceError,
    BadShiftParameterError,
    CellValidationError,
    LoneValueOnMultipleCellsError,
    MissingLabelError,
    OutOfBoundsError,
)
from datachef.lookup.engines.closest import Closest
from datachef.lookup.engines.direct import Directly
from datachef.lookup.engines.within import Within
from datachef.models.source.cell import BaseCell, Cell
from datachef.models.source.table import LiveTable
from datachef.selection import datafuncs as dfc
from datachef.utils.decorators import dontmutate


def _reverse_direction(direction: Direction):
    """
    Helper to reverse the provided direction to help make
    the api conceptually easier for users.
    """

    if direction.name in ["down", "below"]:
        return up
    elif direction.name in ["up", "above"]:
        return down
    elif direction.name == "left":
        return right
    elif direction.name == "right":
        return left
    else:
        raise Exception(f"Unable to identify direction: {direction}")


class Selectable(LiveTable):
    """
    Inherits from LiveTable to add cell selection methods that are generic to all tabulated inputs.
    """

    def assert_one(self):
        """
        Assert that the current selection contains exactly one cell
        """
        assert (
            len(self.cells) == 1
        ), f"Selection contains {len(self.cells)} cells, not 1"
        return self

    def lone_value(self) -> str:
        """
        Confirms the selection contains exactly one cell, then returns
        the value of that cell
        """
        if len(self.cells) != 1:
            raise LoneValueOnMultipleCellsError(
                f"""
                Selection contains {len(self.cells)} cell. It must contain 1 to use .lone_value()
                """
            )
        return self.cells[0].value

    @dontmutate
    def is_blank(self, disregard_whitespace=True):
        """
        Filters the selection to those cells that are blank.
        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the disregard_whitespace keyword.
        """
        self.cells = [
            x
            for x in self.cells
            if x.is_blank(disregard_whitespace=disregard_whitespace)
        ]
        return self

    @dontmutate
    def is_not_blank(self, disregard_whitespace=True):
        """
        Filters the selection to those cells that are not blank.

        By default a cell with just whitespace in it is
        considered blank. You can change this behaviour
        with the disregard_whitespace keyword.
        """
        self.cells = [
            x
            for x in self.cells
            if x.is_not_blank(disregard_whitespace=disregard_whitespace)
        ]
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
        direction._confirm_pristine()
        selection: List[BaseCell] = []

        # To begin with, the potential cells is equal to all cells
        # not currently selected.
        potential_cells: List[Cell] = dfc.cells_not_in(self.pcells, self.cells)

        if direction in [up, down, above, below]:

            # Only consider things on the same horizontal(x) index as a cell
            # that's already selected.
            all_used_x_indicies: FrozenSet[int] = set(c.x for c in self.cells)

            # Now consider each relevant x index
            for xi in all_used_x_indicies:

                # All cells on this index (i.e in this column)
                selected_cells_on_xi = dfc.cells_on_x_index(self.cells, xi)

                # Not currently selected cells on this index
                potential_cells_on_xi: List[Cell] = [
                    c for c in potential_cells if c.x == xi
                ]

                if direction in [up, above]:
                    lowest_used_xi = dfc.maximum_y_offset(selected_cells_on_xi)
                    # Add cells from the potential selection to the
                    # actual selection if they meet the criteria.
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_above(lowest_used_xi)  # above: visually
                    ]

                if direction in [down, below]:
                    largest_used_yi = dfc.minimum_y_offset(selected_cells_on_xi)
                    # Add cells from the potential selection to the
                    # actual selection if they meet the criteria.
                    selection += [
                        c
                        for c in potential_cells_on_xi
                        if c.is_below(largest_used_yi)  # below: visually
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
        Move the entire current selection relatively, examples:

        - .shift(right)
        - .shift(right(5))
        - .shift(2, 6)
        - .shift(-1, 4)

        :param direction_or_x: Either a direction of the raw x offset
        of a direction.
        :param possibly_y: Either none or the raw y offset of a direction
        """

        msg = (
            (
                f"The shift method must be called with one of two types of argument{linesep}"
                f"1.) By passing in an up, down, left, right, above or below direction, "
                f"for example: .shift(up). {linesep}"
                "2.) By passing in two integer arguments, on each for x index change and y index change"
                "example: .shift(1, 2)"
            ),
        )

        if isinstance(direction_or_x, int):
            if not isinstance(possibly_y, int):
                raise BadShiftParameterError(msg)
            x_offset = direction_or_x
            y_offset = possibly_y
        elif isinstance(direction_or_x, BaseDirection):
            assert (
                not possibly_y
            ), "Where passing a direction into shift, that must be the only argument"
            x_offset = direction_or_x.x
            y_offset = direction_or_x.y
        else:
            raise BadShiftParameterError(msg)

        wanted_cells: List[BaseCell] = [
            BaseCell(x=c.x + x_offset, y=c.y + y_offset) for c in self.cells
        ]

        found_cells = dfc.matching_xy_cells(self.pcells, wanted_cells)

        if len(found_cells) == 0 and len(wanted_cells) > 0:
            raise OutOfBoundsError(
                "You are attempting to shift your selection "
                "entirely outside of the boundary of the table."
            )

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
            # TODO - guarantee sensible ordering?

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

        # An excel reference that is a multiple row numbers
        # eg: '4:6'
        elif re.match("^[0-9]+:[0-9]+$", excel_ref):
            start_y = excel_ref.split(":")[0]
            end_y = excel_ref.split(":")[1]
            start_y_index: int = dfc.single_excel_row_to_y_index(start_y)
            end_y_index: int = dfc.single_excel_row_to_y_index(end_y)
            if start_y_index >= end_y_index:
                raise BadExcelReferenceError(
                    f'Excel ref "{excel_ref}" is invalid. {end_y_index} must be higher than {start_y_index}'
                )
            selected = [
                c for c in self.cells if c.y >= start_y_index and c.y <= end_y_index
            ]

        # An excel reference that is one column letter
        # eg: 'H'
        elif re.match("^[A-Z]+$", excel_ref):
            wanted_x_index: int = dfc.single_excel_column_to_x_index(excel_ref)
            selected = [c for c in self.cells if c.x == wanted_x_index]

        # An excel reference that is a range of column letters
        # eg: 'H:J'
        elif re.match("^[A-Z]+:[A-Z]+$", excel_ref):
            left_letters = excel_ref.split(":")[0]
            right_letters = excel_ref.split(":")[1]
            start_x_index: int = dfc.single_excel_column_to_x_index(left_letters)
            end_x_index: int = dfc.single_excel_column_to_x_index(right_letters)
            if start_x_index >= end_x_index:
                raise BadExcelReferenceError(
                    f'Excel ref "{excel_ref}" is invalid. {right_letters} much be higher than {left_letters}'
                )
            selected = [
                c for c in self.cells if c.x >= start_x_index and c.x <= end_x_index
            ]

        # Unknown excel reference
        else:
            raise BadExcelReferenceError(f"Unrecognised excel reference {excel_ref}")

        self.cells = selected
        return self

    def validate(self, validator: BaseValidator, raise_first_error: bool = False):
        """
        Validates current cell selection by passing each currently
        selected cell to the provided validator.

        Pass raise_first_error=True if you just want the first
        invalid value message.
        """

        validation_errors = []
        for cell in self.cells:
            if not validator(cell):
                if raise_first_error:
                    raise CellValidationError(validator.msg(cell))
                else:
                    validation_errors.append(validator.msg(cell))

        if len(validation_errors) > 0:
            raise CellValidationError(f"{linesep}".join(validation_errors))

        return self

    @dontmutate
    def filter(self, check: Callable):
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
            lambda cell: True if re.match(pattern, cell.value) is not None else False
        )

    def finds_observations_directly(self, direction: Direction) -> Directly:
        """
        Creates and returns a class:Directly lookup engine
        that can resolve the correct cell from this selection
        relative to any given observation.
        """

        if not self._label:
            raise MissingLabelError(
                """
                You are trying to create a lookup engine for a selection of
                cells using the .resolve_observations_directly() method but
                have not yet assigned a label to said selection of cells.

                Please use the .label_as() method to assign a label before
                attempting this.
            """
            )

        # The constructor we provide to the user advertises that the column
        # lookup engines "finds the observations" but this is purely a
        # conceptual trick to make a more user friendly api.
        # In reality that's exactly backwards, an observation actually finds
        # a column value (by being passed to the lookup engine constructed below).
        # As such we need to reverse the stated direction.
        return Directly(self.label, self, _reverse_direction(direction))

    def finds_observations_closest(self, direction: Direction) -> Closest:
        """
        Creates and returns a class:Closest lookup engine
        that can resolve the correct cell from this selection
        relative to any given observation.
        """

        if not self._label:
            raise MissingLabelError(
                """
                You are trying to create a lookup engine for a selection of
                cells using the .resolve_observations_closest() method but
                have not yet assigned a label to said selection of cells.

                Please use the .label_as() method to assign a label before
                attempting this.
            """
            )

        # The constructor we provide to the user advertises that the column
        # lookup engines "finds the observations" but this is purely a
        # conceptual trick to make a more user friendly api.
        # In reality that's exactly backwards, an observation actually finds
        # a column value (by being passed to the lookup engine constructed below).
        # As such we need to reverse the stated direction.
        return Closest(self.label, self, _reverse_direction(direction))

    def finds_observations_within(
        self, direction: Direction, start: Direction, end: Direction
    ) -> Within:
        """
        Creates and returns a class:Within lookup engine
        that can resolve the correct cell from this selection
        relative to any given observation.
        """

        if not self.label:
            raise MissingLabelError(
                """
                You are trying to create a lookup engine for a selection of
                cells using the .resolve_observations_within() method but have
                not yet assigned a label to said selection of cells.

                Please use the .label_as() method to assign a label before
                attempting this.
            """
            )

        # The constructor we provide to the user advertises that the column
        # lookup engines "finds the observations" but this is purely a
        # conceptual trick to make a more user friendly api.
        # In reality that's exactly backwards, an observation actually finds
        # a column value (by being passed to the lookup engine constructed below).
        # As such we need to reverse the stated direction.
        # In the case of Within we also need to reverse the direction of
        # parsing and offsetting.
        # new_start = copy.deepcopy(start)
        # new_start.x = 0 - end.x
        # new_start.y = 0 - end.y

        # new_end = copy.deepcopy(end)
        # new_end.x = 0 - start.x
        # new_end.y = 0 - start.y

        return Within(self.label, self, _reverse_direction(direction), start, end)
