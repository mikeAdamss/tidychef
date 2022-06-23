import pytest

from pivoter.cardinal.directions import DOWN, LEFT, RIGHT, UP
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

    s = table_simple_as_xls1.excel_ref("W5:W10").fill(DOWN)
    assert len(s.cells) == 90

    s = table_simple_as_xls1.excel_ref("E2").fill(
        DOWN
    ) - table_simple_as_xls1.excel_ref("E4").fill(DOWN)
    assert len(s.cells) == 2

    s = table_simple_as_xls1.excel_ref("W75").fill(RIGHT).fill(UP)
    assert len(s.cells) == 222

    s = table_simple_as_xls1.excel_ref("D4").fill(
        LEFT
    ) - table_simple_as_xls1.excel_ref("Z4").fill(LEFT)
    assert len(s.cells) == 0
