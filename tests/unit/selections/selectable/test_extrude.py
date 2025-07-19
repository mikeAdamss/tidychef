import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef import datafuncs as dfc
from tidychef.direction.directions import down, left, right, up
from tidychef.exceptions import OutOfBoundsError
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_extrude(selectable_simple1: Selectable):
    """
    Test the extrude method works as expected.
    """

    # extrude down
    extrude_down = selectable_simple1.excel_ref("B6:G6").extrude(down(2))
    extrude_down.assert_len(18)
    assert dfc.basecells_to_excel_ref(extrude_down) == "B6:G8"

    # extrude down
    extrude_up = selectable_simple1.excel_ref("B6:G6").extrude(up)
    extrude_up.assert_len(12)
    assert dfc.basecells_to_excel_ref(extrude_up) == "B5:G6"

    # extrude right
    extrude_right = (
        selectable_simple1.excel_ref("B6:B9") | selectable_simple1.excel_ref("F6:F9")
    ).extrude(right(2))
    extrude_right.assert_len(24)
    # should raise, not quadlitaleral
    with pytest.raises(AssertionError):
        dfc.basecells_to_excel_ref(extrude_right)

    # extrude left
    extrude_left = selectable_simple1.excel_ref("E6:E10").extrude(left(4))
    extrude_left.assert_len(25)
    assert dfc.basecells_to_excel_ref(extrude_left) == "A6:E10"


def test_extrude_out_of_bounds(selectable_simple1: Selectable):
    """
    Test the extrude method raises OutOfBoundsError as expected.
    """

    # extrude down, out of bounds
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("B6:G6").extrude(down(100))

    # extrude up, out of bounds
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("B6:G6").extrude(up(100))

    # extrude right, out of bounds
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("B6:B9").extrude(right(100))

    # extrude left, out of bounds
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("E6:E10").extrude(left(100))


def test_extrude_boundary_cases(selectable_simple1: Selectable):
    """
    Test that extrude raises OutOfBoundsError when attempting to extrude 
    beyond table boundaries, including edge cases.
    """
    
    # Try to extrude right from the rightmost column (Z) - should fail
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("Z50").extrude(right)
    
    # Try to extrude left from the leftmost column (A) - should fail
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("A50").extrude(left)
    
    # Try to extrude up from the top row - should fail
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("M1").extrude(up)
    
    # Try to extrude down from the bottom row (100) - should fail
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("M100").extrude(down)
    
    # Try to extrude with a large distance that goes out of bounds - should fail
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("Y100").extrude(right(5))  # Y+5 = beyond Z
        
    # Even partial extrusion should fail if ANY cell hits a boundary
    # This should raise an error because Z50 cannot extrude further right
    with pytest.raises(OutOfBoundsError):
        selectable_simple1.excel_ref("Y50:Z50").extrude(right)
