import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_row(selectable_simple1: Selectable):
    """
    Test we can select exactly one row from a selection
    """
    selectable_simple1.row("1").assert_single_row()


def test_row_containing_strings(selectable_simple1: Selectable):
    """
    Test we can select exactly one row from a selection
    where the row contains all of the strings in the provided list.
    """
    selectable_simple1.row_containing_strings(["A2val", "D2val"]).assert_single_row()
