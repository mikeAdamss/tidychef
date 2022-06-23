import pytest

from pivoter.cardinal.directions import DOWN, LEFT, RIGHT, UP
from pivoter.exceptions import CellsDoNotExistError
from pivoter.selection import datafuncs as dfc
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


def test_expand(table_simple_as_xls1: XlsInputSelectable):
    """
    Test the expand RIGHT commands work.
    """

    s = table_simple_as_xls1.excel_ref("W5:W10").expand(RIGHT)
    assert len(s.cells) == 24

    s = table_simple_as_xls1.excel_ref("E2:H2").expand(UP)
    assert len(s.cells) == 8

    s = table_simple_as_xls1.excel_ref("X17:Y18").expand(LEFT)
    assert len(s.cells) == 50

    s = (
        table_simple_as_xls1.excel_ref("X5") | table_simple_as_xls1.excel_ref("A2")
    ).expand(DOWN)
    assert len(s.cells) == 195


def test_out_of_bounds_from_excel_ref(table_simple_as_xls1: XlsInputSelectable):
    """
    Test that asking for a cell outside of the boundaries of the
    current table raises a suitable error.
    """

    with pytest.raises(CellsDoNotExistError):
        table_simple_as_xls1.excel_ref("ADFG120909")
