import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()

@pytest.fixture
def selectable_simple1_with_blank_in_bottom_right_corner():
    """
    Fixture for a Selectable with blanks in the data.
    """
    selectable = fixture_simple_one_tab()
    # Blank the very last (bottom right) cell
    selectable.pcells[len(selectable.pcells) - 1].value = ""
    selectable.cells = selectable.pcells
    return selectable

def test_box_select(selectable_simple1: Selectable):
    """
    Test we can select a single box from a selected cel
    """
    selection = selectable_simple1.cell_containing_string("W97val").expand_to_box()
    assert len(selection) == 16

def test_box_select_with_blank(selectable_simple1_with_blank_in_bottom_right_corner: Selectable):
    """
    Test we can select a single box from a selected cell, removing blanks
    """
    selection = selectable_simple1_with_blank_in_bottom_right_corner.cell_containing_string("W97val").expand_to_box()
    assert len(selection) == 15  # 16 values - 1 blank cell

def test_box_select_with_keep_blanks(selectable_simple1_with_blank_in_bottom_right_corner: Selectable):
    """
    Test we can select a single box from a selected cell, not removing blanks
    """
    selection = selectable_simple1_with_blank_in_bottom_right_corner.cell_containing_string("W97val").expand_to_box(remove_blank=False)
    assert len(selection) == 16  # 16 again - 15 non blank cells + 1 blank cell