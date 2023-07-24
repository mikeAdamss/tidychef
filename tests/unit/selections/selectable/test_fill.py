import pytest

from tidychef.direction.directions import down, left, right, up
from tidychef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_expand(selectable_simple1: Selectable):
    """
    Test the expand RIGHT commands work.
    """

    s = selectable_simple1.excel_ref("W5:W10").fill(down)
    assert len(s.cells) == 90

    s = selectable_simple1.excel_ref("E2").fill(down) - selectable_simple1.excel_ref(
        "E4"
    ).fill(down)
    assert len(s.cells) == 2

    s = selectable_simple1.excel_ref("W75").fill(right).fill(up)
    assert len(s.cells) == 222

    s = selectable_simple1.excel_ref("D4").fill(left) - selectable_simple1.excel_ref(
        "Z4"
    ).fill(left)
    assert len(s.cells) == 0
