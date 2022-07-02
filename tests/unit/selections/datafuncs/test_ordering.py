from datachef.models.source.cell import BaseCell
from datachef.selection import datafuncs as dfc


def test_order_cells_leftright_topbottom():
    """
    Given an unordered list of cells, return them in a human readable
    order.

    i.e top row to bottom row, left to right
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_leftright_topbottom(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=0, y=0), BaseCell(x=5, y=2), BaseCell(x=6, y=2), BaseCell(x=2, y=5), BaseCell(x=12, y=12), BaseCell(x=3, y=16)]"
    )


def test_order_cells_rightleft_bottomtop():
    """
    Given an unordered list of cells, return them in a reversed human readable
    order.

    i.e bottom row to top row, right to left
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_rightleft_bottomtop(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=3, y=16), BaseCell(x=12, y=12), BaseCell(x=2, y=5), BaseCell(x=6, y=2), BaseCell(x=5, y=2), BaseCell(x=0, y=0)]"
    )


def test_order_cells_topbottom_leftright():
    """
    Consider a "column" of cells in turn, moveing top to bottom
    from the leftmost column to the rightmost column.
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_topbottom_leftright(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=0, y=0), BaseCell(x=2, y=5), BaseCell(x=3, y=16), BaseCell(x=5, y=2), BaseCell(x=6, y=2), BaseCell(x=12, y=12)]"
    )


def test_order_cells_bottomtop_rightleft():
    """
    Consider a "column" of cells in turn, moveing top to bottom
    from the leftmost column to the rightmost column.
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(6, 14),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_bottomtop_rightleft(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=12, y=12), BaseCell(x=6, y=14), BaseCell(x=6, y=2), BaseCell(x=5, y=2), BaseCell(x=3, y=16), BaseCell(x=2, y=5), BaseCell(x=0, y=0)]"
    )
