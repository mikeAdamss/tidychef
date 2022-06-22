from typing import List

from pivoter.exceptions import CellsDoNotExistError
from pivoter.models.source.cell import BaseCell
from pivoter.utils import cellutils

def matching_xy_cells(
    cells: List[BaseCell], wanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given a list of cells, return all that match xy values
    with those in wanted_cells
    """
    return [x for x in cells if any([x.matches_xy(y) for y in wanted_cells])]


def cells_not_in(initial_cells: List[BaseCell], without_cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given two lists of cells. Return a List[BaseCell] representing
    initial_cells minus any cells from without_cells
    """
    return [c1 for c1 in initial_cells if not any([c1.matches_xy(c2) for c2 in without_cells])]


def exactly_matched_xy_cells(
    cells: List[BaseCell], wanted_cells: List[BaseCell]
) -> List[BaseCell]:
    """
    Given a list of cells, return any that match xy values
    with those in in wanted_cells.

    Raises an exception if we're asking for wanted_cells
    that do not exist.
    """

    unfound_cells = cells_not_in(wanted_cells, cells)

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


def minium_y_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the smallest y position in use
    """
    min_y = min([c.y for c in cells])
    min_y_cell = [c for c in cells if c.y == min_y]
    return min_y_cell[0].y


def maximum_y_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the largest y position in use
    """
    min_y = max([c.y for c in cells])
    min_y_cell = [c for c in cells if c.y == min_y]
    return min_y_cell[0].y


def minimum_x_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the smallest x position in use
    """
    min_x = min([c.x for c in cells])
    min_x_cell = [c for c in cells if c.x == min_x]
    return min_x_cell[0].x


def maximum_x_offset(cells: List[BaseCell]) -> int:
    """
    Given a list of BaseCell's, return the largest x position in use
    """
    max_x = max([c.x for c in cells])
    max_x_cell = [c for c in cells if c.x == max_x]
    return max_x_cell[0].x


def specific_cell_from_xy(cells: List, x: int, y: int) -> BaseCell:
    """
    Given a list of cells and specific x and y co-ordinates,
    return the resuested cell.
    """
    cells_that_match = exactly_matched_xy_cells(cells, [BaseCell(x=x, y=y)])
    assert len(cells_that_match) == 1
    return cells_that_match[0]


def xycells_to_excel_ref(cells: List[BaseCell]) -> str:
    """
    Given a list of cells representing a solid selection with
    no gaps. Return the representative excel reference.
    """

    # +1 to account for zero offsets
    min_x: int = minimum_x_offset(cells)
    max_x: int = maximum_x_offset(cells)
    min_y: int = minium_y_offset(cells)
    max_y: int = maximum_y_offset(cells)

    # Confirm its a contiguous selection with no gaps
    x_axis = (max_x - min_x) + 1
    y_axis = (max_y - min_y) + 1
    assert (x_axis * y_axis) == len(cells)
    
    topleft_cell = specific_cell_from_xy(cells, min_x, min_y)
    bottomright_cell = specific_cell_from_xy(cells, max_x, max_y)

    ref1 = f'{cellutils.x_to_letters(topleft_cell.x)}{cellutils.y_to_number(topleft_cell.y)}'
    ref2 = f'{cellutils.x_to_letters(bottomright_cell.x)}{cellutils.y_to_number(bottomright_cell.y)}'
    return f'{ref1}:{ref2}'

