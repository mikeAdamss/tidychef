import pytest

from tidychef.notebook.preview.boundary import Boundary
from tidychef.selection.selectable import Selectable
from tests.fixtures.preconfigured import fixture_simple_small_one_tab
from tests.unit.helpers import qcel


@pytest.fixture
def selectable_simple_small1():
    return fixture_simple_small_one_tab()


def test_boundary(selectable_simple_small1: Selectable):
    """
    Confirm basic expected behaviour from the Boundary class
    """

    selection = selectable_simple_small1
    boundary = Boundary([selection])

    assert boundary.highest_point == 0
    assert boundary.lowest_point == 19
    assert boundary.leftmost_point == 0
    assert boundary.rightmost_point == 10

    assert boundary.contains(qcel("A2")) is True
    assert boundary.contains(qcel("ZZZ2000")) is False


def test_boundary_bounded_excel_ref(selectable_simple_small1: Selectable):
    """
    Confirm we can specify an explicit boundary from a larger
    table using an excel style reference
    """

    selection = selectable_simple_small1
    boundary = Boundary([selection], bounded="A10:C12")

    assert boundary.highest_point == 9
    assert boundary.lowest_point == 11
    assert boundary.leftmost_point == 0
    assert boundary.rightmost_point == 2


def test_boundary_selection_boundary(selectable_simple_small1: Selectable):
    """
    Confirm that where using selection_boundary=True
    the boundary class adds a one cell buffer around the selection
    """

    selection = selectable_simple_small1.excel_ref("B2")
    boundary = Boundary([selection], selection_boundary=True)

    assert boundary.highest_point == 0
    assert boundary.lowest_point == 2
    assert boundary.leftmost_point == 0
    assert boundary.rightmost_point == 2


def test_boundary_selection_boundary_and_bounded_are_mutually_exclusive(
    selectable_simple_small1: Selectable,
):
    """
    Confirm that where using selection_boundary=True
    and a bounded keyword an assertion error is raised
    """

    selection = selectable_simple_small1

    with pytest.raises(AssertionError):
        Boundary([selection], bounded="A1", selection_boundary=True)
