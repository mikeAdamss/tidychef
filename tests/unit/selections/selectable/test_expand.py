import pytest

from datachef.cardinal.directions import down, left, right, up
from datachef.exceptions import CellsDoNotExistError
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_expand(selectable_simple1: Selectable):
    """
    Test the expand RIGHT commands work.
    """

    s = selectable_simple1.excel_ref("W5:W10").expand(right)
    assert len(s.cells) == 24

    s = selectable_simple1.excel_ref("E2:H2").expand(up)
    assert len(s.cells) == 8

    s = selectable_simple1.excel_ref("X17:Y18").expand(left)
    assert len(s.cells) == 50

    s = (
        selectable_simple1.excel_ref("X5") | selectable_simple1.excel_ref("A2")
    ).expand(down)
    assert len(s.cells) == 195


def test_out_of_bounds_from_excel_ref(selectable_simple1: Selectable):
    """
    Test that asking for a cell outside of the boundaries of the
    current table raises a suitable error.
    """

    with pytest.raises(CellsDoNotExistError):
        selectable_simple1.excel_ref("ADFG120909")
