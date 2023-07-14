import pytest

from datachef.notebook.preview.boundary import Boundary
from datachef.selection.selectable import Selectable
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
