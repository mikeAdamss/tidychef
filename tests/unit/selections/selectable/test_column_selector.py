import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_column(selectable_simple1: Selectable):
    """
    Test we can select exactly one column from a selection
    """
    selectable_simple1.column("C").assert_single_column()


def test_column_containing_strings(selectable_simple1: Selectable):
    """
    Test we can select exactly one column from a selection
    where the column contains all of the strings in the provided list.
    """
    selectable_simple1.column_containing_strings(["A2val", "A5val"]).assert_single_column()