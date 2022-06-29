from os import linesep

import pytest

from datachef.selection.selectable import Selectable
from datachef.utils.preview.boundary import Boundary
from tests.fixtures.preconfigured import fixture_simple_small_one_tab


@pytest.fixture
def selectable_simple_small1():
    return fixture_simple_small_one_tab()


def test_boundary_repr(selectable_simple_small1: Selectable):
    """
    Test that our simple print of the boundary (for debugging)
    works as expected.
    """

    s = selectable_simple_small1.excel_ref("B4:F16")

    b = Boundary([s])
    b_repr = str(b)
    # should be ...
    #        1
    #        |
    # A ---------- K
    #        |
    #        20
    assert "- K" in b_repr
    assert "A " in b_repr

    b = Boundary([s], start="B4", end="F16")
    b_repr = str(b)
    # should be ...
    #        4
    #        |
    # B ---------- F
    #        |
    #        16
    assert "- F" in b_repr
    assert "B " in b_repr
