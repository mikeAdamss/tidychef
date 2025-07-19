from __future__ import annotations

import re
from os import linesep
from typing import Callable, List, Optional, Union

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
from tidychef.utils import cellutils
from tidychef.utils.decorators import dontmutate


class Selectable(LiveTable):
    """
    Inherits from LiveTable to add cell selection methods that are generic to all tabulated inputs.
    """

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
        distinct_rows_count: int = len(dfc.all_used_y_indicies(self.cells))
        assert (
            distinct_rows_count == 1
        ), f"Selection is not from just one row. Got rows: {distinct_rows_count}"
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
        current_cells_set = set(self.cells)  # Single conversion for O(1) lookups
        new_cells = []

        # Use neighbor traversal for much faster expansion
        if direction in [up, above]:
            # For each cell in current selection, traverse up until we hit a boundary
            for cell in self.cells:
                current = cell._neighbour_up
                while current is not None and current not in current_cells_set:
                    new_cells.append(current)
                    current = current._neighbour_up

        elif direction in [down, below]:
            # For each cell in current selection, traverse down until we hit a boundary
            for cell in self.cells:
                current = cell._neighbour_down
                while current is not None and current not in current_cells_set:
                    new_cells.append(current)
                    current = current._neighbour_down

        elif direction == left:
            # For each cell in current selection, traverse left until we hit a boundary
            for cell in self.cells:
                current = cell._neighbour_left
                while current is not None and current not in current_cells_set:
                    new_cells.append(current)
                    current = current._neighbour_left

        elif direction == right:
            # For each cell in current selection, traverse right until we hit a boundary
            for cell in self.cells:
                current = cell._neighbour_right
                while current is not None and current not in current_cells_set:
                    new_cells.append(current)
                    current = current._neighbour_right

        # Remove duplicates and cells that are already in current selection
        current_cells_set = set(self.cells)  # We already have this from above
        seen = set()
        unique_new_cells = []
        for cell in new_cells:
            if cell not in seen and cell not in current_cells_set:
                seen.add(cell)
                unique_new_cells.append(cell)

        # Extend current selection with new cells
        self.cells.extend(unique_new_cells)
        return self

    @dontmutate
    def fill(self, direction: Direction):
        """
        Creates a new selection from the cells in that direction
        relative to the current cell selection.

        :direction: One of: up, down, left, right
        """

        # Fill is just a slightly modified wrapper
        # for expand.

        original_cells_set = set(self.cells)  # Convert to set for faster lookups
        self = self.expand(direction)

        # Use set difference for much faster filtering
        self.cells = [x for x in self.cells if x not in original_cells_set]
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

        # For multi-step moves, break them down into single-step recursive calls
        if abs(x_offset) > 1 or abs(y_offset) > 1:
            # Break down into single steps and apply recursively
            if x_offset != 0:
                x_step = 1 if x_offset > 0 else -1
                self = self.shift(x_step, 0)
                return self.shift(x_offset - x_step, y_offset)
            else:  # y_offset != 0
                y_step = 1 if y_offset > 0 else -1
                self = self.shift(0, y_step)
                return self.shift(x_offset, y_offset - y_step)
        
        # Handle single-step shifts using neighbor traversal (much faster than coordinate lookup)
        found_cells = []
        
        for cell in self.cells:
            shifted_cell = None
            
            # Handle single direction shifts efficiently
            if x_offset == 1 and y_offset == 0:  # right
                shifted_cell = cell._neighbour_right
            elif x_offset == -1 and y_offset == 0:  # left
                shifted_cell = cell._neighbour_left
            elif x_offset == 0 and y_offset == 1:  # down
                shifted_cell = cell._neighbour_down
            elif x_offset == 0 and y_offset == -1:  # up
                shifted_cell = cell._neighbour_up
            
            if shifted_cell:
                found_cells.append(shifted_cell)

        if len(found_cells) == 0 and len(self.cells) > 0:
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
            # We've indexed which cells make up a column as we can just return directly
            wanted_x_index: int = dfc.single_excel_column_to_x_index(excel_ref)
            wanted_column_letters = cellutils.x_to_letters(wanted_x_index)

            # They're asking for a column that doesn't exist
            if wanted_column_letters not in self._column_index:
                raise ReferenceOutsideSelectionError(msg)

            # They're asking for a column that doesn't exist in the current selection
            if wanted_x_index not in set(c.x for c in self.cells):
                raise ReferenceOutsideSelectionError(msg)

            wanted = set(self._column_index[wanted_column_letters])
            selected = [c for c in self.cells if c in wanted]

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
            wanted = []
            for x_offset in range(start_x_index, end_x_index + 1):
                letter = cellutils.x_to_letters(x_offset)

                # They're specifying a column that doesn't exist
                if letter not in self._column_index:
                    raise ReferenceOutsideSelectionError(msg)

                # They're specifying a column that doesn't exist in the current selection
                if x_offset not in set(c.x for c in self.cells):
                    raise ReferenceOutsideSelectionError(msg)

                wanted += self._column_index[letter]
            selected = [c for c in self.cells if c in wanted]

        # Unknown excel reference
        else:
            raise BadExcelReferenceError(f"Unrecognised excel reference: {excel_ref}")

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
        return self

    @dontmutate
    def re(self, pattern: str):
        """
        Filter the current selection of cells to only include
        cells whose value matches the provided regular expression
        pattern.
        """

        matcher = re.compile(pattern)
        self.cells = [x for x in self.cells if matcher.match(str(x.value)) is not None]
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

        # Validation checks (keep existing validation logic)
        if direction.is_vertical:
            if direction.is_downwards:
                highest_y = dfc.maximum_y_offset(self.cells)
                if any(x.y <= highest_y for x in additional_selection.cells):
                    raise AmbiguousWaffleError(
                        "When using waffle down, your additional selections must all "
                        "be below your initial selections."
                    )
            if direction.is_upwards:
                lowest_y = dfc.minimum_y_offset(self.cells)
                if any(x.y >= lowest_y for x in additional_selection.cells):
                    raise AmbiguousWaffleError(
                        "When using waffle up, your additional selections must all be "
                        "above your initial selections."
                    )
        else:
            if direction.is_right:
                highest_x = dfc.maximum_x_offset(self.cells)
                if any(x.x <= highest_x for x in additional_selection.cells):
                    raise AmbiguousWaffleError(
                        "When using waffle right, your additional selections must all "
                        "be right of your initial selections."
                    )
            if direction.is_left:
                lowest_x = dfc.minimum_x_offset(self.cells)
                if any(x.x >= lowest_x for x in additional_selection.cells):
                    raise AmbiguousWaffleError(
                        "When using waffle left, your additional selections must all be "
                        "left of your initial selections."
                    )

        # Use neighbor traversal for much faster waffle intersection
        result_cells = []
        seen_coordinates = set()  # Track coordinates to avoid duplicates during collection
        
        if direction.is_vertical:
            # For vertical waffle: x from current selection, y from additional selection
            # Use neighbor traversal to find cells at intersection coordinates
            additional_y_coords = {cell.y for cell in additional_selection.cells}
            
            for current_cell in self.cells:
                # For each x-coordinate in current selection, find cells at additional y-coordinates
                for target_y in additional_y_coords:
                    target_coord = (current_cell.x, target_y)
                    if target_coord not in seen_coordinates:
                        # Navigate to the target y coordinate using neighbor traversal
                        found_cell = self._navigate_to_coordinate(current_cell, current_cell.x, target_y)
                        if found_cell:
                            result_cells.append(found_cell)
                            seen_coordinates.add(target_coord)
        else:
            # For horizontal waffle: x from additional selection, y from current selection  
            # Use neighbor traversal to find cells at intersection coordinates
            additional_x_coords = {cell.x for cell in additional_selection.cells}
            
            for current_cell in self.cells:
                # For each y-coordinate in current selection, find cells at additional x-coordinates
                for target_x in additional_x_coords:
                    target_coord = (target_x, current_cell.y)
                    if target_coord not in seen_coordinates:
                        # Navigate to the target x coordinate using neighbor traversal
                        found_cell = self._navigate_to_coordinate(current_cell, target_x, current_cell.y)
                        if found_cell:
                            result_cells.append(found_cell)
                            seen_coordinates.add(target_coord)

        self.cells = result_cells
        return self

    def _navigate_to_coordinate(self, start_cell, target_x, target_y):
        """
        Helper method to navigate from start_cell to target coordinates using neighbor traversal.
        Returns the cell at (target_x, target_y) if it exists, None otherwise.
        """
        current = start_cell
        
        # Navigate horizontally first
        while current.x != target_x:
            if current.x < target_x:
                if current._neighbour_right is None:
                    return None  # Can't reach target
                current = current._neighbour_right
            else:
                if current._neighbour_left is None:
                    return None  # Can't reach target
                current = current._neighbour_left
        
        # Now navigate vertically  
        while current.y != target_y:
            if current.y < target_y:
                if current._neighbour_down is None:
                    return None  # Can't reach target
                current = current._neighbour_down
            else:
                if current._neighbour_up is None:
                    return None  # Can't reach target
                current = current._neighbour_up
                
        return current

    @dontmutate
    def extrude(self, direction: Direction):
        """
        Increase selection in a single direction by the amount
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
        current_cells_set = set(self.cells)  # For fast duplicate checking
        seen_additional = set()  # Track additional cells to avoid duplicates during collection

        # Use neighbor traversal for much faster extrusion
        for cell in self.cells:
            current = cell
            
            # Traverse in the specified direction, collecting ALL cells up to the specified distance
            if direction.is_right:
                for step in range(direction.x):
                    current = current._neighbour_right
                    if current is None:
                        # Hit table boundary before completing the full extrusion - this is out of bounds
                        raise OutOfBoundsError(
                            f"You are attempting to extrude your selection beyond the boundary of the table. "
                            f"Cell {cell._excel_ref()} cannot be extruded {direction.x} steps to the right "
                            f"(stopped at step {step + 1})."
                        )
                    if current not in current_cells_set and current not in seen_additional:
                        additional_cells.append(current)
                        seen_additional.add(current)
                        
            elif direction.is_left:
                # For left direction, direction.x is negative, so we take abs()
                for step in range(abs(direction.x)):
                    current = current._neighbour_left
                    if current is None:
                        # Hit table boundary before completing the full extrusion - this is out of bounds
                        raise OutOfBoundsError(
                            f"You are attempting to extrude your selection beyond the boundary of the table. "
                            f"Cell {cell._excel_ref()} cannot be extruded {abs(direction.x)} steps to the left "
                            f"(stopped at step {step + 1})."
                        )
                    if current not in current_cells_set and current not in seen_additional:
                        additional_cells.append(current)
                        seen_additional.add(current)
                        
            elif direction.is_downwards:
                for step in range(direction.y):
                    current = current._neighbour_down
                    if current is None:
                        # Hit table boundary before completing the full extrusion - this is out of bounds
                        raise OutOfBoundsError(
                            f"You are attempting to extrude your selection beyond the boundary of the table. "
                            f"Cell {cell._excel_ref()} cannot be extruded {direction.y} steps downwards "
                            f"(stopped at step {step + 1})."
                        )
                    if current not in current_cells_set and current not in seen_additional:
                        additional_cells.append(current)
                        seen_additional.add(current)
                        
            elif direction.is_upwards:
                # For up direction, direction.y is negative, so we take abs()
                for step in range(abs(direction.y)):
                    current = current._neighbour_up
                    if current is None:
                        # Hit table boundary before completing the full extrusion - this is out of bounds
                        raise OutOfBoundsError(
                            f"You are attempting to extrude your selection beyond the boundary of the table. "
                            f"Cell {cell._excel_ref()} cannot be extruded {abs(direction.y)} steps upwards "
                            f"(stopped at step {step + 1})."
                        )
                    if current not in current_cells_set and current not in seen_additional:
                        additional_cells.append(current)
                        seen_additional.add(current)

        # Add new cells to current selection (no dedup needed since we prevented duplicates above)
        self.cells.extend(additional_cells)
        return self

    def attach_directly(self, direction: Direction) -> Directly:
        """
        Creates and returns a class:Directly lookup engine
        that can resolve the correct cell from this selection
        relative to any given observation.
        """

        if not self._label:
            raise MissingLabelError(
                """
                You are trying to create a lookup engine for a selection of
                cells using the .attach_directly() method but
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

    def attach_closest(self, direction: Direction) -> Closest:
        """
        Creates and returns a class:Closest lookup engine
        that can resolve the correct cell from this selection
        relative to any given observation.
        """

        if not self._label:
            raise MissingLabelError(
                """
                You are trying to create a lookup engine for a selection of
                cells using the .attach_closest() method but
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

    def attach_within(
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
                cells using the .attach_within() method but have
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

    @dontmutate
    def row(self, row_number: int):
        """
        Specifies a selection of cells from the current selection that are
        all on the specfied row.
        """
        return self.excel_ref(row_number)

    @dontmutate
    def row_containing_strings(self, row_strings: List[str], strict=True):
        """
        Specifies a selection of cells from the current selection that are
        all on the same row - but - only where there's at least one cell
        on that row contains each of the strings in the provided list.
        """
        assert isinstance(
            row_strings, list
        ), "You must provide a list of strings to row_containing_strings"

        found_cells = []
        for y_index in dfc.all_used_y_indicies(self.cells):
            row_cells = dfc.cells_on_y_index(self.cells, y_index)
            found_count = 0
            for wanted in row_strings:
                if strict:
                    # If strict, wanted must be exactly equal to the cell value
                    row_values = {cell.value for cell in row_cells}  # Use set for O(1) lookup
                    if wanted in row_values:
                        found_count += 1
                else:
                    # If not strict a substring match is fine
                    for cell in row_cells:
                        if wanted in cell.value:
                            found_count += 1
                            break
            if found_count == len(row_strings):
                # If we found at least one instance of everying on this row, add it to the selection
                found_cells += row_cells

        self.cells = found_cells
        self.assert_single_row()

        return self

    @dontmutate
    def column(self, column_letter: str):
        """
        Returns a new selection of cells that are all in the same
        column as the first cell in the current selection.
        """
        return self.excel_ref(column_letter)

    @dontmutate
    def column_containing_strings(self, column_strings: List[str]):
        """
        Specifies a selection of cells from the current selection that are
        all in the same column - but - only where there's at least one cell
        in that column containing each of the strings in the provided list.
        """
        found_cells = []
        for x_index in dfc.all_used_x_indicies(self.cells):
            column_cells = dfc.cells_on_x_index(self.cells, x_index)
            column_values = {cell.value for cell in column_cells}  # Use set for O(1) lookup
            found_count = 0
            for wanted in column_strings:
                if wanted in column_values:
                    found_count += 1
            if found_count == len(column_strings):
                # If we found all the strings in this column, add it to the selection
                found_cells += column_cells

        self.cells = found_cells
        self.assert_single_column()

        return self

    @dontmutate
    def expand_to_box(self, remove_blank: bool = True):
        """
        Returns a new selection of cells that are all in the same
        region as the first cell in the current selection.

        A region method must always start with a single cell
        and expands as per human reading style, so is effectively an
        alias for.

        single_cell.expand(right).expand(down).is_not_blank()
        """
        self.assert_one()
        if remove_blank:
            cells = self.expand(right).expand(down).is_not_blank().cells
        else:
            cells = self.expand(right).expand(down).cells
        self.cells = cells
        return self

    @dontmutate
    def is_numeric(self):
        """
        Filters the selection to those cells that are numeric.
        """
        self.cells = [x for x in self.cells if x.numeric]
        return self

    @dontmutate
    def is_not_numeric(self):
        """
        Filters the selection to those cells that are not numeric.
        """
        self.cells = [x for x in self.cells if not x.numeric]
        return self

    @dontmutate
    def cell_containing_string(self, string: str, strict: bool = True):
        """
        Filters the selection to precisely one cell containing or equal to the provided string.
        """
        if strict:
            found_cells = [x for x in self.cells if string == x.value]
        else:
            found_cells = [x for x in self.cells if string in x.value]
        self.cells = found_cells
        self.assert_one()
        return self

    @dontmutate
    def cells_containing_string(self, string: str, strict: bool = True):
        """
        Filters the selection to those cells that contain or are equal to the provided strings.
        """
        if strict:
            found_cells = [x for x in self.cells if x.value == string]
        else:
            found_cells = [x for x in self.cells if string in x.value]
        self.cells = found_cells
        return self
