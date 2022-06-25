import pytest

from pivoter.selection.base import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


def test_assert_one_with_single_cell(table_simple_as_xls1: Selectable):
    """
    Test assert one behaves correctly on a selection consisting
    of one cell
    """

    s = table_simple_as_xls1.excel_ref("F93")
    s.assert_one()


def test_assert_one_without_single_cell(table_simple_as_xls1: Selectable):
    """
    Test assert one behaves correctly on a selection not consisiting
    of a single cell.
    """

    with pytest.raises(AssertionError):
        s = table_simple_as_xls1.excel_ref("F93:G94")
        s.assert_one()
