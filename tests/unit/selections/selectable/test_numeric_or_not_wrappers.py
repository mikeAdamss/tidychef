import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


@pytest.fixture
def selectable_simple1_with_one_numeric_cell():
    """
    Fixture that adds one numeric cell to selectable_simple1
    """

    selectable = fixture_simple_one_tab()
    # Cahnge the very last (bottom right) cell
    selectable.pcells[len(selectable.pcells) - 1].value = "2"
    selectable.cells = selectable.pcells
    return selectable

def test_is_numeric(selectable_simple1_with_one_numeric_cell: Selectable):
    """
    Test we can filter a selection to only numeric cells.
    """
    selection = selectable_simple1_with_one_numeric_cell.is_numeric()
    assert len(selection) == 1


def test_is_not_numeric(selectable_simple1, selectable_simple1_with_one_numeric_cell: Selectable):
    """
    Test we can filter a selection to only non-numeric cells.
    """
    selection = selectable_simple1_with_one_numeric_cell.is_not_numeric()
    assert len(selection) == len(selectable_simple1) -1