import pytest

from pivoter.cardinal.directions import UP, DOWN, LEFT, RIGHT
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import fixture_simple_one_tab

from pivoter.selection import datafuncs as dfc


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
