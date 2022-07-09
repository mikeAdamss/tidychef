"""
Helpers to order a list of cells to represent different ways you
could read a tablulated display of data in a cell by cell fashion.
"""

from typing import List

from datachef.models.source.cell import BaseCell


def order_cells_leftright_topbottom(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given a list of BaseCell's sort them into a typical human readable order.

    Example cell read order:
    |  1  |  2  |  3  |
    |  4  |  5  |  6  |

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.y, cell.x), reverse=False)


def order_cells_rightleft_bottomtop(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given a list of BaseCell's sort them into a reverse human readable order.

    Example cell read order:
    |  6  |  5  |  4  |
    |  3  |  2  |  1  |

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.y, cell.x), reverse=True)


def order_cells_topbottom_leftright(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Consider a "column" of cells in turn, moveing top to bottom
    from the leftmost column to the rightmost column.

    Example cell read order:
    |  1  |  3  |  5  |
    |  2  |  4  |  6  |

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.x, cell.y), reverse=False)


def order_cells_bottomtop_rightleft(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Consider a "column" of cells in turn, moveing bottom to top
    from the rightmost column to the leftmost column.

    Example cell read order:
    |  6  |  4  |  2  |
    |  5  |  3  |  1  |

    :param cells: Representing a selection from a tabular data source.
    """
    return sorted(cells, key=lambda cell: (cell.x, cell.y), reverse=True)
