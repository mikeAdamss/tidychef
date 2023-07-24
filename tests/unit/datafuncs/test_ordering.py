from tidychef import datafuncs as dfc
from tidychef.models.source.cell import BaseCell


def test_order_cells_leftright_topbottom():
    """
    Example cell read order:
    |  1  |  2  |  3  |
    |  4  |  5  |  6  |
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
    Example cell read order:
    |  6  |  5  |  4  |
    |  3  |  2  |  1  |
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
    Example cell read order:
    |  1  |  3  |  5  |
    |  2  |  4  |  6  |
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
    Example cell read order:
    |  6  |  4  |  2  |
    |  5  |  3  |  1  |
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


def test_order_cells_rightleft_topbottom():
    """
    Example cell read order:
    |  3  |  2  |  1  |
    |  6  |  5  |  4  |
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(11, 12),
        BaseCell(2, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(6, 14),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_rightleft_topbottom(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=3, y=16), BaseCell(x=6, y=14), BaseCell(x=12, y=12), BaseCell(x=11, y=12), BaseCell(x=2, y=12), BaseCell(x=2, y=5), BaseCell(x=6, y=2), BaseCell(x=5, y=2), BaseCell(x=0, y=0)]"
    )


def test_order_cells_topbottom_rightleft():
    """
    Example cell read order:
    |  5  |  3  |  1  |
    |  6  |  4  |  2  |
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(11, 12),
        BaseCell(2, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(6, 14),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_topbottom_rightleft(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=0, y=0), BaseCell(x=6, y=2), BaseCell(x=5, y=2), BaseCell(x=2, y=5), BaseCell(x=12, y=12), BaseCell(x=11, y=12), BaseCell(x=2, y=12), BaseCell(x=6, y=14), BaseCell(x=3, y=16)]"
    )


def test_order_cells_leftright_bottomtop():
    """
    Example cell read order:
    |  2  |  4  |  6  |
    |  1  |  3  |  5  |
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(11, 12),
        BaseCell(2, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(6, 14),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_leftright_bottomtop(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=0, y=0), BaseCell(x=2, y=12), BaseCell(x=2, y=5), BaseCell(x=3, y=16), BaseCell(x=5, y=2), BaseCell(x=6, y=14), BaseCell(x=6, y=2), BaseCell(x=11, y=12), BaseCell(x=12, y=12)]"
    )


def test_order_cells_bottomtop_leftright():
    """
    Example cell read order:
    |  4  |  5  |  6  |
    |  1  |  2  |  3  |
    """
    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(11, 12),
        BaseCell(2, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(6, 14),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.order_cells_bottomtop_leftright(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=3, y=16), BaseCell(x=6, y=14), BaseCell(x=2, y=12), BaseCell(x=11, y=12), BaseCell(x=12, y=12), BaseCell(x=2, y=5), BaseCell(x=5, y=2), BaseCell(x=6, y=2), BaseCell(x=0, y=0)]"
    )
