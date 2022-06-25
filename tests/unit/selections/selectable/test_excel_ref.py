import pytest

from pivoter.exceptions import (CellsDoNotExistError,
                                LoneValueOnMultipleCellsError)
from pivoter.selection.base import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_lone_value_selector(selectable_simple1: Selectable):
    """
    Test we can return the value for selections of exactly one cell
    """
    assert selectable_simple1.excel_ref("A1").lone_value() == "A1val"


def test_lone_value_on_multiple_values_errors(
    selectable_simple1: Selectable,
):
    """
    Test than calling Input.lone_value() on a filtered table containing
    more than one value raises.
    """

    with pytest.raises(LoneValueOnMultipleCellsError):
        selectable_simple1.excel_ref("A1:A2").lone_value()


def test_excel_referece_out_of_bounds_error(
    selectable_simple1: Selectable,
):
    """
    Test that we cannot select using an excel reference for cells that
    are not within the current selection
    """

    with pytest.raises(CellsDoNotExistError) as exc_info:
        selectable_simple1.excel_ref("AA2")
