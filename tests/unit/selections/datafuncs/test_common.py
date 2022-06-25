import pytest
from typing import List

from pivoter.models.source.cell import BaseCell, Cell
from pivoter.selection.base import Selectable
from pivoter.selection import datafuncs as dfc
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_matching_xy_cells(selectable_simple1: Selectable):
    """
    Test we can ask for and recieve specific cells from with a table
    """

    msg = 'cannot find {} in {}'

    find = [BaseCell(0,1), BaseCell(0, 2)] # A2 and A3
    found: List[Cell] = dfc.matching_xy_cells(selectable_simple1.cells, find)
    assert len(found) == 2
    for cell in found:
        exp = ['A2val', 'A3val']
        assert cell.value in exp, msg.format(cell.value, exp)

    find = [BaseCell(3,4), BaseCell(8, 16)] # D3 and H17
    found: List[Cell] = dfc.matching_xy_cells(selectable_simple1.cells, find)
    assert len(found) == 2
    for cell in found:
        exp = ['D5val', 'I17val']
        assert cell.value in exp, msg.format(cell.value, exp)

