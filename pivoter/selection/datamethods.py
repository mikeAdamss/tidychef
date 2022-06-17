from typing import List

from pivoter.exceptions import CellsDoNotExistError
from pivoter.models.source.cell import BaseCell

class DataMethods:
    """
    The data selection and combination methods that power
    _all_ data selection and combination methods.

    We're exposing these to account for unknown or complex use
    cases, but otherwise push the user towards the more
    obvious and user friendly methods (which are ultimately just
    wrappers of these).
    """

    @classmethod
    def _matching_xy_cells_from_filtered(
        cls, input, wanted_cells: List[BaseCell]
    ) -> List[BaseCell]:
        """
        Given a list of class:BaseCell's, get all cells from input.selected_table.filtered,
        that match xy values with cells in wanted_cells
        """
        return [
            x
            for x in input.selected_table.filtered.cells
            if any([x.matches_xy(y) for y in wanted_cells])
        ]

    @classmethod
    def _exactly_matched_xy_cells_from_filtered(
        cls, input, wanted_cells: List[BaseCell]
    ) -> List[BaseCell]:
        """
        Given a list of class:BaseCell's, get all cells from input.selected_table.filtered,
        that match xy values with cells in wanted_cells.

        Raises an exception if we're asking for Cells that do not currently appear in
        input.selected_table.filtered
        """

        matched_cells = cls._matching_xy_cells_from_filtered(input, wanted_cells)
        unfound_cells = [x for x in wanted_cells if not any([x.matches_xy(y) for y in matched_cells])]
        if len(unfound_cells) > 1:
            raise CellsDoNotExistError(input.cfg, unfound_cells)

        return cls._matching_xy_cells_from_filtered(input, wanted_cells)

    @classmethod
    def _cells_on_x_index(cls, input, x: int) -> List[BaseCell]:
        """
        Return a list of cells from input.selected_table.filtered that
        are on the specific x index
        """
        return [c for c in input.selected_table.filtered if c.x == x]

    @classmethod
    def _cells_on_y_index(cls, input, y: int) -> List[BaseCell]:
        """
        Return a list of cells from input.selected_table.filtered that
        are on the specific y index
        """
        return [c for c in input.selected_table.filtered if c.y == y]
