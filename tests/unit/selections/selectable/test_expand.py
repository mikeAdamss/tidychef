import pytest

from pivoter.cardinal.directions import DOWN, LEFT, RIGHT, UP
from pivoter.exceptions import CellsDoNotExistError
from pivoter.selection.base import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_expand(selectable_simple1: Selectable):
    """
    Test the expand RIGHT commands work.
    """

    s = selectable_simple1.excel_ref("W5:W10").expand(RIGHT)
    assert len(s.cells) == 24

    s = selectable_simple1.excel_ref("E2:H2").expand(UP)
    assert len(s.cells) == 8

    s = selectable_simple1.excel_ref("X17:Y18").expand(LEFT)
    assert len(s.cells) == 50

    s = (
        selectable_simple1.excel_ref("X5") | selectable_simple1.excel_ref("A2")
    ).expand(DOWN)
    assert len(s.cells) == 195


def test_out_of_bounds_from_excel_ref(selectable_simple1: Selectable):
    """
    Test that asking for a cell outside of the boundaries of the
    current table raises a suitable error.
    """

    with pytest.raises(CellsDoNotExistError):
        selectable_simple1.excel_ref("ADFG120909")
