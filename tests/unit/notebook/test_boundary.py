import pytest

from datachef.exceptions import PreviewBoundarySpecificationError
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


def test_boundary_bounded_positional_dict(selectable_simple_small1: Selectable):
    """
    Confirm we can specify an explicit boundary from a larger
    table using an excel style reference
    """

    selection = selectable_simple_small1
    boundary = Boundary([selection], bounded={"start_xy": "0,9", "end_xy": "2,11"})

    assert boundary.highest_point == 9
    assert boundary.lowest_point == 11
    assert boundary.leftmost_point == 0
    assert boundary.rightmost_point == 2


def test_boundary_bounded_exceptions(selectable_simple_small1: Selectable):
    """
    Confirms that passing incorrect arguments to the
    Boundary class results in the expected errors.
    """

    selection = selectable_simple_small1

    # Wrong type for bounded
    with pytest.raises(PreviewBoundarySpecificationError):
        Boundary([selection], bounded=5)

    # Wrong keys for dict to bounded
    with pytest.raises(PreviewBoundarySpecificationError):
        Boundary([selection], bounded={"foo": "bar"})

    # Missing values for dict to bounded
    with pytest.raises(PreviewBoundarySpecificationError):
        Boundary([selection], bounded={"start_xy": "bar"})

    # Incorrectly formatted values for dict to bounded
    with pytest.raises(PreviewBoundarySpecificationError):
        Boundary([selection], bounded={"start_xy": "0,0", "end_xy": "00"})

    # Incorrectly formatted values with non numeric types
    with pytest.raises(PreviewBoundarySpecificationError):
        Boundary([selection], bounded={"start_xy": "0,B", "end_xy": "0,2"})

    # End value of selection it above or left of the start value
    with pytest.raises(PreviewBoundarySpecificationError):
        Boundary([selection], bounded={"start_xy": "10,10", "end_xy": "0,0"})
