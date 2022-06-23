import pytest

from pivoter.exceptions import CellsDoNotExistError, LoneValueOnMultipleCellsError
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import fixture_simple_one_tab, fixture_simple_two_tabs


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


@pytest.fixture
def sheet_of_two_tables():
    return fixture_simple_two_tabs()



def test_lone_value_selector(table_simple_as_xls1: XlsInputSelectable):
    """
    Test we can return the value for selections of exactly one cell
    """
    assert table_simple_as_xls1.excel_ref("A1").lone_value() == "A1val"


def test_lone_value_on_multiple_values_errors(
    table_simple_as_xls1: XlsInputSelectable,
):
    """
    Test than calling Input.lone_value() on a filtered table containing
    more than one value raises.
    """

    with pytest.raises(LoneValueOnMultipleCellsError):
        table_simple_as_xls1.excel_ref('A1:A2').lone_value()


def test_excel_referece_out_of_bounds_error(
    table_simple_as_xls1: XlsInputSelectable,
):
    """
    Test that we cannot select using an excel reference for cells that
    are not within the current selection
    """

    with pytest.raises(CellsDoNotExistError) as exc_info:
        table_simple_as_xls1.excel_ref("AA2")
