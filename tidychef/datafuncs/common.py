"""
Common data functions that do not fall into any of the other categories.
"""
from typing import List, Tuple

from tidychef.exceptions import CellsDoNotExistError
from tidychef.models.source.cell import BaseCell


def assert_quadrilaterals(cells: List[BaseCell]) -> Tuple[int, int, int, int]:
    """
    Assert that the provided list of cells equates to selection of cells
    that form a quadrilateral shape with no gaps.

    This is a requirement when attempting to create an excel reference
    representing a list of cells.

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A tuple of ints, min_x, max_x, min_y, max_y.
    """

    min_x, max_x, min_y, max_y = get_outlier_indicies(cells)

    x_axis = (max_x - min_x) + 1
    y_axis = (max_y - min_y) + 1

    assert (x_axis * y_axis) == len(
        cells
    ), "The provided selection of cells does not equate to a quadrilateral selection"

    return min_x, max_x, min_y, max_y


def cell_is_within(cells: List[BaseCell], cell: BaseCell) -> bool:
    """
    Is the cell present within the list of cells

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :param cell: A BaseCell or inheritor of that represents a single selected cell.
    :return: bool, is the cell in the cells list.
    """
    find_cell = matching_xy_cells(cells, [cell])
    return len(find_cell) == 1


def cell_is_not_within(cells: List[BaseCell], cell: BaseCell) -> bool:
    """
    Is the cell absent from the list of cells

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :param cell: A BaseCell or inheritor of that represents a single selected cell.
    :return: bool, is the cell absent from the cells list.
    """
    return not cell_is_within(cells, cell)


def cells_not_in(
    initial_cells: List[BaseCell], unwanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given two lists of cells. Return a List[BaseCell] representing
    initial_cells minus any cells from unwanted_cells

    :param initial_cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :param unwanted_cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: The cells from initial cells minus any that were in unwanted_cells
    """
    return [
        c1
        for c1 in initial_cells
        if not any(c1.matches_xy(c2) for c2 in unwanted_cells)
    ]


def cells_on_x_index(cells: List[BaseCell], x_index: int) -> List[BaseCell]:
    """
    Return a list from the provided cells that are on the specific x index.

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :xi: A horizontal index, the column number of a tabulated data source
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    return [c for c in cells if c.x == x_index]


def cells_on_y_index(cells: List[BaseCell], y_index: int) -> List[BaseCell]:
    """
    Return a list from the provided cells that are on the specific y index

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :param yi: A horizontal index, the column number of a tabulated data source
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    return [c for c in cells if c.y == y_index]


def exactly_matched_xy_cells(
    cells: List[BaseCell], wanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given a list of cells, return any that match xy values
    with those in in wanted_cells.

    Raises an exception if we're asking for wanted_cells
    that do not exist.

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """

    unfound_cells = cells_not_in(wanted_cells, cells)

    if len(unfound_cells) > 0:
        raise CellsDoNotExistError(
            f"""
            Cannot find cell(s):
            {unfound_cells}

            In existing cells:
            {cells}
        """
        )

    return matching_xy_cells(cells, wanted_cells)


def exactly_matching_xy_cell(cells: List[BaseCell], wanted_cell: BaseCell) -> BaseCell:
    """
    Given a wanted cell, the cell from cells that matches xy values
    with it

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A single BaseCell or inheritor of.
    """
    match = [c1 for c1 in cells if any([c1.matches_xy(wanted_cell)])]
    assert len(match) == 1
    return match[0]


def get_outlier_indicies(cells: List[BaseCell]) -> Tuple[int, int, int, int]:
    """
    Given a list of cells, returns maximum and minimum x and y
    values from cells within that selection.

    returns:
    - min_x
    - max_x
    - min_y
    - max_y

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A tuple of ints, min_x, max_x, min_y, max_y.
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

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    return [c1 for c1 in cells if any(c1.matches_xy(c2) for c2 in wanted_cells)]


def maximum_x_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the largest x position in use

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: The maximum horizontal index in use
    """
    max_x = max(c.x for c in cells)
    max_x_cell = [c for c in cells if c.x == max_x]
    return max_x_cell[0].x


def maximum_y_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the largest y position in use

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: The maximum vertical index in use.
    """
    max_y = max(c.y for c in cells)
    max_y_cell = [c for c in cells if c.y == max_y]
    return max_y_cell[0].y


def minimum_x_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the smallest x position in use

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: The minimum horizontal index in use.
    """
    min_x = min(c.x for c in cells)
    min_x_cell = [c for c in cells if c.x == min_x]
    return min_x_cell[0].x


def minimum_y_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the smallest y position in use

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: The maximum vertical index in use.
    """
    min_y = min(c.y for c in cells)
    min_y_cell = [c for c in cells if c.y == min_y]
    return min_y_cell[0].y


def specific_cell_from_xy(
    cells: List[BaseCell], x_index: int, y_index: int
) -> BaseCell:
    """
    Given a list of cells and specific x and y co-ordinates,
    return the requested cell.

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A single BaseCell or inheritor of.
    """
    cells_that_match = exactly_matched_xy_cells(cells, [BaseCell(x=x_index, y=y_index)])
    assert len(cells_that_match) == 1
    return cells_that_match[0]


def all_used_x_indicies(cells: List[BaseCell]) -> List[int]:
    """
    Given a list of cells, return each unique x indicies
    for a "row" that contains at least one cell.

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of every horizontal index (x attribute) present in cells.
    """
    return list(set((cell.x for cell in cells)))


def all_used_y_indicies(cells: List[BaseCell]) -> List[int]:
    """
    Given a list of cells, return each unique y indicies
    for a "column" that contains at least one cell.

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of every vertical index (y attribute) present in cells.
    """
    return list(set((cell.y for cell in cells)))
