import pytest

from pivoter.cardinal.directions import DOWN, LEFT, RIGHT, UP
from pivoter.selection.base import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_expand(selectable_simple1: Selectable):
    """
    Test the expand RIGHT commands work.
    """

    s = selectable_simple1.excel_ref("W5:W10").fill(DOWN)
    assert len(s.cells) == 90

    s = selectable_simple1.excel_ref("E2").fill(DOWN) - selectable_simple1.excel_ref(
        "E4"
    ).fill(DOWN)
    assert len(s.cells) == 2

    s = selectable_simple1.excel_ref("W75").fill(RIGHT).fill(UP)
    assert len(s.cells) == 222

    s = selectable_simple1.excel_ref("D4").fill(LEFT) - selectable_simple1.excel_ref(
        "Z4"
    ).fill(LEFT)
    assert len(s.cells) == 0
