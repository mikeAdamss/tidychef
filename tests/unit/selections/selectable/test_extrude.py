import pytest

from datachef.direction.directions import down, left, right, up
from datachef import datafuncs as dfc
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_extrude(selectable_simple1: Selectable):
    """
    Test the extrude method works as expected.
    """

    # extrude down
    extrude_down = selectable_simple1.excel_ref("B6:G6").extrude(down(2))
    extrude_down.assert_len(18)
    assert dfc.basecells_to_excel_ref(extrude_down) == "B6:G8"

    # extrude down
    extrude_up = selectable_simple1.excel_ref("B6:G6").extrude(up)
    extrude_up.assert_len(12)
    assert dfc.basecells_to_excel_ref(extrude_up) == "B5:G6"

    # extrude right
    extrude_right = (selectable_simple1.excel_ref("B6:B9") | selectable_simple1.excel_ref("F6:F9")).extrude(right(2))
    extrude_right.assert_len(24)
    # should raise, not quadlitaleral
    with pytest.raises(AssertionError):
        dfc.basecells_to_excel_ref(extrude_right)

    # extrude left
    extrude_left = selectable_simple1.excel_ref("E6:E10").extrude(left(4))
    extrude_left.assert_len(25)
    assert dfc.basecells_to_excel_ref(extrude_left) == "A6:E10"
