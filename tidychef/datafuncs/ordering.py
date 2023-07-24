"""
Helpers to order a list of cells to represent different ways you
could read a tablulated display of data in a cell by cell fashion.
"""

from typing import List

import tidychef.datafuncs as dfc
from tidychef.models.source.cell import BaseCell


def order_cells_leftright_topbottom(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given a list of BaseCell's sort them into a typical human readable order.

    Example cell read order:
    |  1  |  2  |  3  |
    |  4  |  5  |  6  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    return sorted(cells, key=lambda cell: (cell.y, cell.x), reverse=False)


def order_cells_rightleft_bottomtop(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Given a list of BaseCell's sort them into a reverse human readable order.

    Example cell read order:
    |  6  |  5  |  4  |
    |  3  |  2  |  1  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    return sorted(cells, key=lambda cell: (cell.y, cell.x), reverse=True)


def order_cells_topbottom_leftright(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Order cells moving top to bottom from the leftmost column to the
    rightmost column.

    Example cell read order:
    |  1  |  3  |  5  |
    |  2  |  4  |  6  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    return sorted(cells, key=lambda cell: (cell.x, cell.y), reverse=False)


def order_cells_bottomtop_rightleft(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Order cells moving bottom to top from the rightmost column to the
    leftmost column.

    Example cell read order:
    |  6  |  4  |  2  |
    |  5  |  3  |  1  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    return sorted(cells, key=lambda cell: (cell.x, cell.y), reverse=True)


def order_cells_rightleft_topbottom(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Order cells left to right moving from the bottom row to the
    top row.

    Example cell read order:
    |  3  |  2  |  1  |
    |  6  |  5  |  4  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    maximum_y = max(cell.y for cell in cells)
    maximum_x = max(cell.x for cell in cells)

    ordered_cells = []
    for y_index in range(maximum_y + 1, -1, -1):
        for x_index in range(maximum_x + 1, -1, -1):
            wanted_cell = BaseCell(x=x_index, y=y_index)
            if dfc.cell_is_within(cells, wanted_cell):
                ordered_cells.append(
                    dfc.specific_cell_from_xy(cells, x_index=x_index, y_index=y_index)
                )
    return ordered_cells


def order_cells_topbottom_rightleft(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Order cells right to left moving from the lefthand to right columns
    considering cells top to bottom

    Example cell read order:
    |  5  |  3  |  1  |
    |  6  |  4  |  2  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    maximum_y = max(cell.y for cell in cells)
    maximum_x = max(cell.x for cell in cells)

    ordered_cells = []
    for y_index in range(0, maximum_y + 1):
        for x_index in range(maximum_x + 1, -1, -1):
            wanted_cell = BaseCell(x=x_index, y=y_index)
            if dfc.cell_is_within(cells, wanted_cell):
                ordered_cells.append(
                    dfc.specific_cell_from_xy(cells, x_index=x_index, y_index=y_index)
                )
    return ordered_cells


def order_cells_leftright_bottomtop(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Order cells left to right moving from the left to righthand columns
    considering cells bottom to top

    Example cell read order:
    |  2  |  4  |  6  |
    |  1  |  3  |  5  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    maximum_y = max(cell.y for cell in cells)
    maximum_x = max(cell.x for cell in cells)

    ordered_cells = []
    for x_index in range(0, maximum_x + 1):
        for y_index in range(maximum_y + 1, -1, -1):
            wanted_cell = BaseCell(x=x_index, y=y_index)
            if dfc.cell_is_within(cells, wanted_cell):
                ordered_cells.append(
                    dfc.specific_cell_from_xy(cells, x_index=x_index, y_index=y_index)
                )
    return ordered_cells


def order_cells_bottomtop_leftright(cells: List[BaseCell]) -> List[BaseCell]:
    """
    Order cells from bottom row to top row moving from left to right

    Example cell read order:
    |  4  |  5  |  6  |
    |  1  |  2  |  3  |

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """
    maximum_y = max(cell.y for cell in cells)
    maximum_x = max(cell.x for cell in cells)

    ordered_cells = []
    for y_index in range(maximum_y + 1, -1, -1):
        for x_index in range(0, maximum_x + 1):
            wanted_cell = BaseCell(x=x_index, y=y_index)
            if dfc.cell_is_within(cells, wanted_cell):
                ordered_cells.append(
                    dfc.specific_cell_from_xy(cells, x_index=x_index, y_index=y_index)
                )
    return ordered_cells
