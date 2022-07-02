from socketserver import ThreadingUnixDatagramServer
from typing import List

from datachef.models.source.cell import BaseCell


def order_cells_leftright_topbottom(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given a list of BaseCell's sort them into a typical human readable order,
    defined as:
    - Reading each row from top to bottom
    - Read each cell from left to right

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.y, cell.x), reverse=False)


def order_cells_rightleft_bottomtop(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given a list of BaseCell's sort them into a reverse human readable order,
    defined as:
    - Reading each row from bottom to top
    - Read each cell from right to left

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.y, cell.x), reverse=True)


def order_cells_topbottom_leftright(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Consider a "column" of cells in turn, moveing top to bottom
    from the leftmost column to the rightmost column.

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.x, cell.y), reverse=False)


def order_cells_bottomtop_rightleft(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Consider a "column" of cells in turn, moveing bottom to top
    from the rightmost column to the leftmost column.

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.x, cell.y), reverse=True)
