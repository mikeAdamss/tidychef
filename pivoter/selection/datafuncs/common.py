from typing import List

from pivoter.exceptions import CellsDoNotExistError
from pivoter.models.source.cell import BaseCell



def matching_xy_cells(cells: List[BaseCell], wanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given a list of cells, return all that match xy values
    with those in wanted_cells
    """
    return [x for x in cells if any([x.matches_xy(y) for y in wanted_cells])]


def cells_not_in(cells: List[BaseCell], looked_for: List[BaseCell]
) -> List[BaseCell]:
    """
    Given two lists of cells. Return those cells from looked_for
    that do not appear in cells
    """
    return [c1 for c1 in looked_for if not any([c1.matches_xy(c2) for c2 in cells])]


def exactly_matched_xy_cells(cells: List[BaseCell], wanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given a list of cells, return any that match xy values
    with those in in wanted_cells.

    Raises an exception if we're asking for wanted_cells
    that do not exist.
    """

    unfound_cells = cells_not_in(cells, wanted_cells)

    if len(unfound_cells) > 0:
        raise CellsDoNotExistError(unfound_cells)

    return matching_xy_cells(cells, wanted_cells)


def cells_on_x_index(cells: List[BaseCell], x: int) -> List[BaseCell]:
    """
    Return a list from the provided cells that are on the specific x index
    """
    return [c for c in cells if c.x == x]


def cells_on_y_index(cells: List[BaseCell], y: int) -> List[BaseCell]:
    """
    Return a list from the provided cells that are on the specific y index
    """
    return [c for c in cells if c.y == y]


def minium_y_offset_cell(cells: List[BaseCell]) -> BaseCell:
    """
    Given a list of BaseCell's, return the Basecell with the smallest
    y offset
    """
    min_y = min([c.y for c in cells])
    min_y_cell = [c for c in cells if c.y == min_y]
    assert len(min_y_cell) == 1
    return min_y_cell[0]


def maximum_y_offset_cell(cells: List[BaseCell]) -> BaseCell:
    """
    Given a list of BaseCell's, return the Basecell with the largest
    y offset
    """
    min_y = max([c.y for c in cells])
    min_y_cell = [c for c in cells if c.y == min_y]
    assert len(min_y_cell) == 1
    return min_y_cell[0]


def minimum_x_offset_cell(cells: List[BaseCell]) -> BaseCell:
    """
    Given a list of BaseCell's, return the Basecell with the smallest
    y offset
    """
    min_x = min([c.x for c in cells])
    min_x_cell = [c for c in cells if c.x == min_x]
    assert len(min_x_cell) == 1
    return min_x_cell[0]


def maximum_x_offset_cell(cells: List[BaseCell]) -> BaseCell:
    """
    Given a list of BaseCell's, return the Basecell with the largest
    x offset
    """
    max_x = max([c.x for c in cells])
    max_x_cell = [c for c in cells if c.x == max_x]
    assert len(max_x_cell) == 1
    return max_x_cell[0]
