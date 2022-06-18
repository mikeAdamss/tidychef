from typing import List

from pivoter.exceptions import CellsDoNotExistError
from pivoter.models.source.cell import BaseCell


class DataMethods:
    """
    The data selection and combination methods that power
    _all_ data selection and combination methods.

    We're exposing these via .datamethods to account for
    unknown or complex use cases for advanced users, but
    otherwise we push the user towards the more
    obvious and user friendly methods attached to the
    various source type specific selecors (which are
    ultimately just wrappers of these more low level
    methods).
    """

    @classmethod
    def _matching_xy_cells(
        cls, cells: List[BaseCell], wanted_cells: List[BaseCell]
    ) -> List[BaseCell]:
        """
        Given a list of cells, return all that match xy values
        with those in wanted_cells
        """
        return [x for x in cells if any([x.matches_xy(y) for y in wanted_cells])]

    @classmethod
    def _cells_not_in(
        cls, list1: List[BaseCell], list2: List[BaseCell]
    ) -> List[BaseCell]:
        """
        Given two lists of cells. Return those cells from list2
        that do not appear in list1
        """
        return [x for x in list2 if not any([x.matches_xy(y) for y in list1])]

    @classmethod
    def _exactly_matched_xy_cells(
        cls, cells: List[BaseCell], wanted_cells: List[BaseCell]
    ) -> List[BaseCell]:
        """
        Given a list of cells, return any that match xy values
        with those in in wanted_cells.

        Raises an exception if we're asking for wanted_cells
        that do not exist.
        """

        matched_cells = cls._matching_xy_cells(cells, wanted_cells)
        unfound_cells = [
            x for x in wanted_cells if not any([x.matches_xy(y) for y in matched_cells])
        ]
        if len(unfound_cells) > 1:
            raise CellsDoNotExistError(5, unfound_cells)

        return cls._matching_xy_cells(cells, wanted_cells)

    @classmethod
    def _cells_on_x_index(cls, cells: List[BaseCell], x: int) -> List[BaseCell]:
        """
        Return a list from the provided cells that are on the specific x index
        """
        return [c for c in cells if c.x == x]

    @classmethod
    def _cells_on_y_index(cls, cells: List[BaseCell], y: int) -> List[BaseCell]:
        """
        Return a list from the provided cells that are on the specific y index
        """
        return [c for c in cells if c.y == y]

    @classmethod
    def _minium_y_offset_cell(cls, cells: List[BaseCell]) -> BaseCell:
        """
        Given a list of BaseCell's, return the Basecell with the smallest
        y offset
        """
        min_y = min([c.y for c in cells])
        min_y_cell = [c for c in cells if c.y == min_y]
        assert len(min_y_cell) == 1
        return min_y_cell[0]

    @classmethod
    def _maximum_y_offset_cell(cls, cells: List[BaseCell]) -> BaseCell:
        """
        Given a list of BaseCell's, return the Basecell with the largest
        y offset
        """
        min_y = max([c.y for c in cells])
        min_y_cell = [c for c in cells if c.y == min_y]
        assert len(min_y_cell) == 1
        return min_y_cell[0]
