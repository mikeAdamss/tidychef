import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_cell_selector(selectable_simple1: Selectable):
    """
    Test we can select a single cell from a selection.
    """
    selection = selectable_simple1.cell_containing_string("W97val")
    assert len(selection) == 1
    assert selection.cells[0].value == "W97val"


def test_cell_selector_not_strict(selectable_simple1: Selectable):
    """
    Test we can select a single cell from a selection, not strictly.
    """
    selection = selectable_simple1.column("W").cell_containing_string("97val", strict=False)
    assert len(selection) == 1
    assert selection.cells[0].value == "W97val"