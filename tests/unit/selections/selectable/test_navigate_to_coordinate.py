import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_navigate_to_coordinate_basic_movement(selectable_simple1: Selectable):
    """
    Test basic horizontal and vertical movement with _navigate_to_coordinate.
    """
    # Start with a cell at B2 (x=1, y=1)
    selection = selectable_simple1.excel_ref("B2")
    start_cell = selection.cells[0]
    
    # Test moving right
    target_cell = selection._navigate_to_coordinate(start_cell, 3, 1)  # D2
    assert target_cell is not None
    assert target_cell.x == 3
    assert target_cell.y == 1
    
    # Test moving left
    target_cell = selection._navigate_to_coordinate(start_cell, 0, 1)  # A2
    assert target_cell is not None
    assert target_cell.x == 0
    assert target_cell.y == 1
    
    # Test moving down
    target_cell = selection._navigate_to_coordinate(start_cell, 1, 4)  # B5
    assert target_cell is not None
    assert target_cell.x == 1
    assert target_cell.y == 4
    
    # Test moving up
    target_cell = selection._navigate_to_coordinate(start_cell, 1, 0)  # B1
    assert target_cell is not None
    assert target_cell.x == 1
    assert target_cell.y == 0


def test_navigate_to_coordinate_diagonal_movement(selectable_simple1: Selectable):
    """
    Test diagonal movement (combination of horizontal and vertical).
    """
    # Start with a cell at C3 (x=2, y=2)
    selection = selectable_simple1.excel_ref("C3")
    start_cell = selection.cells[0]
    
    # Test moving diagonally down-right
    target_cell = selection._navigate_to_coordinate(start_cell, 5, 6)  # F7
    assert target_cell is not None
    assert target_cell.x == 5
    assert target_cell.y == 6
    
    # Test moving diagonally up-left
    target_cell = selection._navigate_to_coordinate(start_cell, 0, 0)  # A1
    assert target_cell is not None
    assert target_cell.x == 0
    assert target_cell.y == 0
    
    # Test moving diagonally up-right
    target_cell = selection._navigate_to_coordinate(start_cell, 7, 0)  # H1
    assert target_cell is not None
    assert target_cell.x == 7
    assert target_cell.y == 0
    
    # Test moving diagonally down-left
    target_cell = selection._navigate_to_coordinate(start_cell, 0, 8)  # A9
    assert target_cell is not None
    assert target_cell.x == 0
    assert target_cell.y == 8


def test_navigate_to_coordinate_same_position(selectable_simple1: Selectable):
    """
    Test navigation to the same coordinate (no movement required).
    """
    selection = selectable_simple1.excel_ref("E5")
    start_cell = selection.cells[0]
    
    # Navigate to the same position
    target_cell = selection._navigate_to_coordinate(start_cell, start_cell.x, start_cell.y)
    assert target_cell is not None
    assert target_cell is start_cell  # Should return the exact same cell object
    assert target_cell.x == start_cell.x
    assert target_cell.y == start_cell.y


def test_navigate_to_coordinate_out_of_bounds(selectable_simple1: Selectable):
    """
    Test navigation to coordinates that are out of bounds (should return None).
    
    Note: The simple.csv fixture typically goes from A1 to Z100, so we test beyond those bounds.
    """
    selection = selectable_simple1.excel_ref("A1")
    start_cell = selection.cells[0]
    
    # Try to navigate left from A1 (should be impossible)
    target_cell = selection._navigate_to_coordinate(start_cell, -1, 0)
    assert target_cell is None
    
    # Try to navigate up from A1 (should be impossible)
    target_cell = selection._navigate_to_coordinate(start_cell, 0, -1)
    assert target_cell is None
    
    # Test from a corner cell - try to go beyond the available data
    selection_corner = selectable_simple1.excel_ref("Z100")  # Bottom-right corner
    corner_cell = selection_corner.cells[0]
    
    # Try to navigate right from Z column (should fail if Z is the last column)
    target_cell = selection._navigate_to_coordinate(corner_cell, 26, 99)  # AA100
    assert target_cell is None
    
    # Try to navigate down from row 100 (should fail if 100 is the last row)  
    target_cell = selection._navigate_to_coordinate(corner_cell, 25, 100)  # Z101
    assert target_cell is None


def test_navigate_to_coordinate_large_distances(selectable_simple1: Selectable):
    """
    Test navigation across large distances to ensure the method handles long traversals.
    """
    # Start from A1
    selection = selectable_simple1.excel_ref("A1")
    start_cell = selection.cells[0]
    
    # Navigate to the opposite corner (Z100)
    target_cell = selection._navigate_to_coordinate(start_cell, 25, 99)  # Z100
    assert target_cell is not None
    assert target_cell.x == 25
    assert target_cell.y == 99
    
    # Navigate from middle to another distant point
    selection_mid = selectable_simple1.excel_ref("M50")  # Middle-ish
    mid_cell = selection_mid.cells[0]
    
    # Go to A1 from middle
    target_cell = selection._navigate_to_coordinate(mid_cell, 0, 0)  # A1
    assert target_cell is not None
    assert target_cell.x == 0
    assert target_cell.y == 0
    
    # Go to Z100 from middle
    target_cell = selection._navigate_to_coordinate(mid_cell, 25, 99)  # Z100
    assert target_cell is not None
    assert target_cell.x == 25
    assert target_cell.y == 99


def test_navigate_to_coordinate_edge_cases(selectable_simple1: Selectable):
    """
    Test edge cases like navigating from edge cells.
    """
    # Test from top edge
    selection_top = selectable_simple1.excel_ref("M1")
    top_cell = selection_top.cells[0]
    
    # Should be able to move horizontally along the top edge
    target_cell = selection_top._navigate_to_coordinate(top_cell, 0, 0)  # A1
    assert target_cell is not None
    assert target_cell.x == 0
    assert target_cell.y == 0
    
    # Test from left edge
    selection_left = selectable_simple1.excel_ref("A50")
    left_cell = selection_left.cells[0]
    
    # Should be able to move vertically along the left edge
    target_cell = selection_left._navigate_to_coordinate(left_cell, 0, 0)  # A1
    assert target_cell is not None
    assert target_cell.x == 0
    assert target_cell.y == 0
    
    # Should be able to move horizontally from left edge
    target_cell = selection_left._navigate_to_coordinate(left_cell, 10, 49)  # K50
    assert target_cell is not None
    assert target_cell.x == 10
    assert target_cell.y == 49


def test_navigate_to_coordinate_consistency(selectable_simple1: Selectable):
    """
    Test that navigation is consistent regardless of starting point when targeting the same coordinate.
    """
    # Define a target coordinate
    target_x, target_y = 10, 15  # K16
    
    # Start from different positions and navigate to the same target
    start_positions = ["A1", "Z1", "A100", "M50", "E20"]
    
    target_cells = []
    for start_pos in start_positions:
        selection = selectable_simple1.excel_ref(start_pos)
        start_cell = selection.cells[0]
        target_cell = selection._navigate_to_coordinate(start_cell, target_x, target_y)
        
        if target_cell is not None:  # Only check if navigation was successful
            target_cells.append(target_cell)
            assert target_cell.x == target_x
            assert target_cell.y == target_y
    
    # All successful navigations should lead to the same cell object
    if len(target_cells) > 1:
        first_target = target_cells[0]
        for other_target in target_cells[1:]:
            assert other_target is first_target, "Navigation from different starting points should lead to the same cell object"


def test_navigate_to_coordinate_neighbor_integrity(selectable_simple1: Selectable):
    """
    Test that the navigation doesn't break neighbor relationships.
    """
    selection = selectable_simple1.excel_ref("E5")
    start_cell = selection.cells[0]
    
    # Navigate to a nearby cell
    target_cell = selection._navigate_to_coordinate(start_cell, 7, 8)  # H9
    assert target_cell is not None
    
    # Verify that the target cell has proper neighbor relationships
    if target_cell._neighbour_right is not None:
        assert target_cell._neighbour_right.x == target_cell.x + 1
        assert target_cell._neighbour_right.y == target_cell.y
    
    if target_cell._neighbour_left is not None:
        assert target_cell._neighbour_left.x == target_cell.x - 1
        assert target_cell._neighbour_left.y == target_cell.y
    
    if target_cell._neighbour_down is not None:
        assert target_cell._neighbour_down.x == target_cell.x
        assert target_cell._neighbour_down.y == target_cell.y + 1
    
    if target_cell._neighbour_up is not None:
        assert target_cell._neighbour_up.x == target_cell.x
        assert target_cell._neighbour_up.y == target_cell.y - 1


def test_navigate_to_coordinate_return_types(selectable_simple1: Selectable):
    """
    Test that the method returns the correct types in all cases.
    """
    selection = selectable_simple1.excel_ref("C3")
    start_cell = selection.cells[0]
    
    # Valid navigation should return a Cell object
    target_cell = selection._navigate_to_coordinate(start_cell, 5, 5)
    assert target_cell is not None
    # Check that it has the expected attributes of a Cell
    assert hasattr(target_cell, 'x')
    assert hasattr(target_cell, 'y')
    assert hasattr(target_cell, 'value')
    assert isinstance(target_cell.x, int)
    assert isinstance(target_cell.y, int)
    
    # Invalid navigation should return None
    invalid_target = selection._navigate_to_coordinate(start_cell, -5, -5)
    assert invalid_target is None
