from __future__ import annotations

import copy
import os
import re
from os import linesep
from pathlib import Path
from typing import Callable, FrozenSet, List, Optional, Union

from tidychef import datafuncs as dfc
from tidychef.against.implementations.base import BaseValidator
from tidychef.direction.directions import (
    BaseDirection,
    Direction,
    above,
    below,
    down,
    left,
    right,
    up,
)
from tidychef.exceptions import (
    AmbiguousWaffleError,
    BadExcelReferenceError,
    BadShiftParameterError,
    CellsDoNotExistError,
    CellValidationError,
    LoneValueOnMultipleCellsError,
    MissingLabelError,
    OutOfBoundsError,
    ReferenceOutsideSelectionError,
)
from tidychef.lookup.engines.closest import Closest
from tidychef.lookup.engines.direct import Directly
from tidychef.lookup.engines.within import Within
from tidychef.models.source.cell import BaseCell, Cell
from tidychef.models.source.table import LiveTable
from tidychef.notebook.preview.html.main import preview
from tidychef.utils.decorators import dontmutate


class Selectable(LiveTable):
    """
    Inherits from LiveTable to add cell selection methods that are generic to all tabulated inputs.
    """

    def config(self, explain=False, explain_path: Optional[Union[str, Path]] = None):
        assert not all(
            [explain, explain_path]
        ), f"""
            Where you have specified explain_path= you do not need
            to also include explain=True. The keywords are mutually
            exclusive.
        """

        if explain_path is not None:
            if isinstance(explain_path, str):
                explain_path = Path(explain_path)
            if explain_path.exists():
                os.remove(explain_path.resolve())  # pragma: no cover

        self._explain_path = explain_path
        self._explain = explain

        return copy.deepcopy(self)

    def _get_excel_references(self) -> List[str]:
        """
        Returns a list of excel references for all selected cells in
        classical human readable order (left to right, top row to bottom row)
        """
        cells: List[Cell] = dfc.order_cells_leftright_topbottom(self.cells)
        return [x._excel_ref() for x in cells]

    def print_excel_refs(self):  # pragma: no cover
        """
        Orders cells in classical human readable order
        (right to left, top row to bottom row) then
        prints a list of ll excel references as a list
        """
        print(self._get_excel_references())

    def assert_len(self, number_of_cells: int):
        """
        Assert that the current selection contains the number of cells
        specified
        """
        assert (
            len(self.cells) == number_of_cells
        ), f"Selection contains {len(self.cells)} cells, not {number_of_cells}"
        _explain(self, f"WALK: Assert selection length is {number_of_cells}")
        return self

    def assert_one(self):
        """
        Assert that the current selection contains exactly one cell
        """
        return self.assert_len(1)

    def assert_single_column(self):
        """
        Assert that all CURRENTLY selected cells are contained in
        a single column.
        """
        assert (
            len(dfc.all_used_x_indicies(self.cells)) == 1
        ), "Selection has cells from more than one column"
        return self

    def assert_single_row(self):
        """
        Assert that all CURRENTLY selected cells are contained on
        a single row.
        """
        assert (
            len(dfc.all_used_y_indicies(self.cells)) == 1
        ), "Selection has cells from more than one row"
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
        _explain(self, f"Is blank")
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
        _explain(self, f"Is not blank")
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
        _explain(self, f"Expand: {direction.name}")
        return self

    @dontmutate
    def fill(self, direction: Direction):
        """
        Creates a new selection from the cells in that direction
        relative to the current cell selection.

        :direction: One of: up, down, left, right
        """

        # Fill is just a slightly modified wrapper
        # for expand. So if ._explain is on we need
        # to toggle if off while doing the expand
        # to avoid confusing the user
        explain_setting = self._explain
        explain_path_setting = self._explain_path
        self._explain = False
        self._explain_path = None

        did_have = copy.deepcopy(self.cells)
        self = self.expand(direction)

        self._explain = explain_setting
        self._explain_path = explain_path_setting

        self.cells = [x for x in self.cells if x not in did_have]
        _explain(self, f"Fill: {direction.name}")
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

        if not possibly_y:
            _explain(self, f"Shifted cells {direction_or_x.offset_as_str}")
        else:
            _explain(self, f"Shifted cells {direction_or_x}, {possibly_y}")
        return self

    @dontmutate
    def excel_ref(self, excel_ref: str):
        """
        Selects just the cells as indicated by the provided excel style
        reference: "A6", "B17:B24", "9", "GH" etc.
        """

        msg = f"""
                You cannot make a selection of "{excel_ref}" at
                this time. One or more cells of these cells
                does not exist in your CURRENT SELECTION.
                
                If you believe they should be, you need to check
                your sequencing.

                As an example: if you filter a selection to just
                column A then try excel_ref('B') you'll get
                this error.

                Where practical, you can debug the selected cells
                at any given time with <selection>.print_excel_refs()
                """

        # Multi excel reference:
        # eg: 'B2:F5'
        if re.match("^[A-Z]+[0-9]+:[A-Z]+[0-9]+$", excel_ref):
            cell1 = dfc.single_excel_ref_to_basecell(excel_ref.split(":")[0])
            cell2 = dfc.single_excel_ref_to_basecell(excel_ref.split(":")[1])
            try:
                assert cell1.x >= self.minimum_pristine_x
                assert cell1.x <= self.maximum_pristine_x
                assert cell1.y >= self.minimum_pristine_y
                assert cell1.y <= self.maximum_pristine_y
                assert cell2.x >= self.minimum_pristine_x
                assert cell2.x <= self.maximum_pristine_x
                assert cell2.y >= self.minimum_pristine_y
                assert cell2.y <= self.maximum_pristine_y
                wanted: List[BaseCell] = dfc.multi_excel_ref_to_basecells(excel_ref)
                selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
            except CellsDoNotExistError:
                raise ReferenceOutsideSelectionError(msg)
            except AssertionError:
                raise ReferenceOutsideSelectionError(msg)

        # Single column and row reference
        # eg: 'F19'
        elif re.match("^[A-Z]+[0-9]+$", excel_ref):
            wanted: BaseCell = dfc.single_excel_ref_to_basecell(excel_ref)
            wanted = [wanted]
            try:
                selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
            except CellsDoNotExistError:
                raise ReferenceOutsideSelectionError(msg)

        # An excel reference that is a single row number
        # eg: '4'
        elif re.match("^[0-9]+$", excel_ref):
            wanted_y_index: int = dfc.single_excel_row_to_y_index(excel_ref)
            wanted = [c for c in self.pcells if c.y == wanted_y_index]
            try:
                assert wanted_y_index <= self.maximum_pristine_y
                assert wanted_y_index >= self.minimum_pristine_y
                selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
            except CellsDoNotExistError:
                raise ReferenceOutsideSelectionError(msg)
            except AssertionError:
                raise ReferenceOutsideSelectionError(msg)

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
            try:
                assert end_y_index <= self.maximum_pristine_y
                assert start_y_index >= self.minimum_pristine_y
                wanted = [
                    c
                    for c in self.pcells
                    if c.y >= start_y_index and c.y <= end_y_index
                ]
                selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
            except CellsDoNotExistError:
                raise ReferenceOutsideSelectionError(msg)
            except AssertionError:
                raise ReferenceOutsideSelectionError(msg)

        # An excel reference that is one column letter
        # eg: 'H'
        elif re.match("^[A-Z]+$", excel_ref):
            wanted_x_index: int = dfc.single_excel_column_to_x_index(excel_ref)
            try:
                assert wanted_x_index <= self.maximum_pristine_x
                assert wanted_x_index >= self.minimum_pristine_x
                wanted = [c for c in self.pcells if c.x == wanted_x_index]
                selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
            except CellsDoNotExistError:
                raise ReferenceOutsideSelectionError(msg)
            except AssertionError:
                raise ReferenceOutsideSelectionError(msg)

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
            wanted = [
                c for c in self.pcells if c.x >= start_x_index and c.x <= end_x_index
            ]
            try:
                assert end_x_index <= self.maximum_pristine_x
                assert start_x_index >= self.minimum_pristine_x
                selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
            except CellsDoNotExistError:
                raise ReferenceOutsideSelectionError(msg)
            except AssertionError:
                raise ReferenceOutsideSelectionError(msg)

        # Unknown excel reference
        else:
            raise BadExcelReferenceError(f"Unrecognised excel reference: {excel_ref}")

        self.cells = selected
        _explain(self, f"Excel reference: {excel_ref}")
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
                    raise CellValidationError(
                        f"""
When making selections from table: {self.name} the
following validation error was encountered:
{validator.msg(cell)}
                """
                    )
                else:
                    validation_errors.append(validator.msg(cell))

        if len(validation_errors) > 0:
            raise CellValidationError(
                f"""
When making selections from table: {self.name} the
following validation errors were encountered:
{linesep.join(validation_errors)}
                """
            )

        return self

    @dontmutate
    def filter(self, check: Callable):
        """
        Selects just the cells that match the provided check

        : param check: a function, lambda or callable class that
        returns a bool when given a single cell as a parameter.
        """

        self.cells = list(filter(check, self.cells))
        if hasattr(check, "explain"):
            comment = check.explain
        else:
            comment = "Custom filter"
        _explain(self, f"Filtered: {comment}")
        return self

    @dontmutate
    def re(self, pattern: str):
        """
        Filter the current selection of cells to only include
        cells whose value matches the provided regular expression
        pattern.
        """

        matcher = re.compile(r"" + pattern)
        self.cells = [x for x in self.cells if matcher.match(x.value) is not None]
        _explain(self, f"Regex, pattern {pattern}")
        return self

    @dontmutate
    def waffle(self, direction: Direction, additional_selection: Selectable):
        """
        A "waffle" will select all cells that directionally intersect
        with both a cell in the current selection and a cell in the
        selection being passed into this method.

        Examples:

        [B1].waffle("A6") == [B6]

        [C4,C5,C6].waffle("F1", "G1") == [F4,F5,F6,G4,G5,G6]
        """

        if direction.is_vertical:
            if direction.is_downwards:
                highest_y = dfc.maximum_y_offset(self.cells)
                if any([x for x in additional_selection if x.y <= highest_y]):
                    raise AmbiguousWaffleError(
                        "When using waffle down, your additional selections must all "
                        "be below your initial selections."
                    )
            if direction.is_upwards:
                lowest_y = dfc.minimum_y_offset(self.cells)
                if any([x for x in additional_selection if x.y >= lowest_y]):
                    raise AmbiguousWaffleError(
                        "When using waffle up, your additional selections must all be "
                        "above your initial selections."
                    )
            x_offsets = dfc.all_used_x_indicies(self.cells)
            y_offsets = dfc.all_used_y_indicies(additional_selection.cells)
        else:
            if direction.is_right:
                highest_x = dfc.maximum_x_offset(self.cells)
                if any([x for x in additional_selection if x.x <= highest_x]):
                    raise AmbiguousWaffleError(
                        "When using waffle right, your additional selections must all "
                        "be right of your initial selections."
                    )
            if direction.is_left:
                lowest_x = dfc.minimum_x_offset(self.cells)
                if any([x for x in additional_selection if x.x >= lowest_x]):
                    raise AmbiguousWaffleError(
                        "When using waffle left, your additional selections must all be "
                        "left of your initial selections."
                    )
            x_offsets = dfc.all_used_x_indicies(additional_selection.cells)
            y_offsets = dfc.all_used_y_indicies(self.cells)

        self.cells = [x for x in self.pcells if x.x in x_offsets and x.y in y_offsets]

        return self

    @dontmutate
    def extrude(self, direction: Direction):
        """
        Increase selection in a single direction s by the amount
        passed as an argument to direction. Where no integer
        parameter is passed into direction, the size of the
        extrusion is one.

        Examples:

        .extrude(right(2)) - increase selection by all cells
        that are within two cells right of a currently selected
        cell.

        .extrude(down(3)) - increase selection by all cells
        that are within three cells down of a currently selected
        cell.

        .extrude(left) - increase selection by select all
        cells that are one cell left of a currently selected cell.

        :param direction: A direction of up, down, left, right,
        above below with optional offset parameter.
        """

        additional_cells = []
        for cell in self.cells:

            if direction.is_horizontal:
                viable_cells = dfc.cells_on_y_index(self.pcells, cell.y)
                if direction.is_right:
                    extruded_cells = [
                        x
                        for x in viable_cells
                        if x.x > cell.x and x.x <= (cell.x + direction.x)
                    ]
                    additional_cells + extruded_cells
                if direction.is_left:
                    extruded_cells = [
                        x
                        for x in viable_cells
                        if x.x < cell.x and x.x >= (cell.x + direction.x)
                    ]
                additional_cells += extruded_cells

            else:
                viable_cells = dfc.cells_on_x_index(self.pcells, cell.x)
                if direction.is_downwards:
                    extruded_cells = [
                        x
                        for x in viable_cells
                        if x.y > cell.y and x.y <= (cell.y + direction.y)
                    ]
                if direction.is_upwards:
                    extruded_cells = [
                        x
                        for x in viable_cells
                        if x.y < cell.y and x.y >= (cell.y + direction.y)
                    ]
                additional_cells += extruded_cells

        self.cells += [x for x in additional_cells if x not in self.cells]
        _explain(self, f"Extrude: {direction.offset_as_str}")
        return self

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
        return Directly(self.label, self, direction.inverted())

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
        return Closest(self.label, self, direction.inverted())

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

        return Within(
            self.label,
            self,
            direction.inverted(),
            start.inverted(),
            end.inverted(),
            table=self.name,
        )


def _explain(selectable: Selectable, comment: str):
    if selectable._explain or selectable._explain_path:
        assert len(selectable.cells) > 0, (
            f'Error: stage "EXPLAIN: {comment}" results in 0 cells selected.'
            " You cannot preview nothing."
        )
        selectable = selectable.label_as(f"EXPLAIN: {comment}")
        preview(selectable, selection_boundary=True, path=selectable._explain_path)
