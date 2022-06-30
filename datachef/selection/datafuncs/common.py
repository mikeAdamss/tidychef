"""
Common data functions that do not fall into any of the other categories.
"""
from typing import List, Optional, Tuple

from datachef.exceptions import CellsDoNotExistError
from datachef.models.source.cell import BaseCell


def assert_quadrilaterals(cells: List[BaseCell]) -> Optional[Tuple[int, int, int, int]]:
    """
    Assert that the provided list of cells equtes to selection of cells
    that form a quadrilateral shape with no gaps.

    This is a requirement when attempting to create an excel reference
    representing a list of cells.
    """

    min_x, max_x, min_y, max_y = get_outlier_indicies(cells)

    x_axis = (max_x - min_x) + 1
    y_axis = (max_y - min_y) + 1

    assert (x_axis * y_axis) == len(
        cells
    ), "The priovided selection of cells does not equate to a quadrilateral selection"

    return min_x, max_x, min_y, max_y


def cell_is_within(cells: List[BaseCell], cell: BaseCell) -> bool:
    """Is the cell present within the list of cells?"""
    find_cell = matching_xy_cells(cells, [cell])
    return len(find_cell) == 1


def cell_is_not_within(cells: List[BaseCell], cell: BaseCell) -> bool:
    """Is the cell absent from the list of cells?"""
    return not cell_is_within(cells, cell)


def cells_not_in(
    initial_cells: List[BaseCell], without_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given two lists of cells. Return a List[BaseCell] representing
    initial_cells minus any cells from without_cells
    """
    return [
        c1 for c1 in initial_cells if not any(c1.matches_xy(c2) for c2 in without_cells)
    ]


def cells_on_x_index(cells: List[BaseCell], xi: int) -> List[BaseCell]:
    """
    Return a list from the provided cells that are on the specific x index.

    :param cells: Representing a selection from a tabular data source.
    :xi: A horizontal index, the column number of a tabulated data source
    """
    return [c for c in cells if c.x == xi]


def cells_on_y_index(cells: List[BaseCell], yi: int) -> List[BaseCell]:
    """
    Return a list from the provided cells that are on the specific y index

    :param cells: Representing a selection from a tabular data source.
    :yi: A horizontal index, the column number of a tabulated data source
    """
    return [c for c in cells if c.y == yi]


def ensure_human_read_order(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given a list of BaseCell's sort them into a typical human readable order,
    defined as:
    - Reading each row from top to bottom
    - Read each cell from left to right

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.y, cell.x), reverse=False)


def exactly_matched_xy_cells(
    cells: List[BaseCell], wanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given a list of cells, return any that match xy values
    with those in in wanted_cells.

    Raises an exception if we're asking for wanted_cells
    that do not exist.

    :param cells: Representing a selection from a tabular data source.
    """

    unfound_cells = cells_not_in(wanted_cells, cells)

    if len(unfound_cells) > 0:
        raise CellsDoNotExistError(unfound_cells)

    return matching_xy_cells(cells, wanted_cells)


def exactly_matching_xy_cell(cells: List[BaseCell], wanted_cell: BaseCell) -> BaseCell:
    """
    Given a wanted cell, the cell from cells that matches xy values
    with it

    :param cells: Representing a selection from a tabular data source.
    """
    match = [c1 for c1 in cells if any([c1.matches_xy(wanted_cell)])]
    assert len(match) == 1
    return match[0]


def get_outlier_indicies(cells: List[BaseCell]) -> Tuple[int, int, int, int]:
    """
    Given a list of cells, returns maximum and minimum x and y
    values from cells within that selecton.

    :param cells: Representing a selection from a tabular data source.
    """
    min_x: int = minimum_x_offset(cells)
    max_x: int = maximum_x_offset(cells)
    min_y: int = minimum_y_offset(cells)
    max_y: int = maximum_y_offset(cells)
    return min_x, max_x, min_y, max_y


def matching_xy_cells(
    cells: List[BaseCell], wanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given a list of cells, return all that match xy values
    with those in wanted_cells.

    Note: does NOT raise an exception if we're asking for wanted_cells
    that do not exist.

    :param cells: Representing a selection from a tabular data source.
    """
    return [c1 for c1 in cells if any(c1.matches_xy(c2) for c2 in wanted_cells)]


def maximum_x_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the largest x position in use

    :param cells: Representing a selection from a tabular data source.
    """
    max_x = max(c.x for c in cells)
    max_x_cell = [c for c in cells if c.x == max_x]
    return max_x_cell[0].x


def maximum_y_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the largest y position in use

    :param cells: Representing a selection from a tabular data source.
    """
    min_y = max(c.y for c in cells)
    min_y_cell = [c for c in cells if c.y == min_y]
    return min_y_cell[0].y


def minimum_x_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the smallest x position in use

    :param cells: Representing a selection from a tabular data source.
    """
    min_x = min(c.x for c in cells)
    min_x_cell = [c for c in cells if c.x == min_x]
    return min_x_cell[0].x


def minimum_y_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the smallest y position in use

    :param cells: Representing a selection from a tabular data source.
    """
    min_y = min(c.y for c in cells)
    min_y_cell = [c for c in cells if c.y == min_y]
    return min_y_cell[0].y


def specific_cell_from_xy(cells: List[BaseCell], x: int, y: int) -> BaseCell:
    """
    Given a list of cells and specific x and y co-ordinates,
    return the requested cell.

    :param cells: Representing a selection from a tabular data source.
    """
    cells_that_match = exactly_matched_xy_cells(cells, [BaseCell(x=x, y=y)])
    assert len(cells_that_match) == 1
    return cells_that_match[0]
