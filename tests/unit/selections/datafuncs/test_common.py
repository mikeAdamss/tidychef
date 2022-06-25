from dataclasses import dataclass
from typing import List

import pytest

from pivoter.models.source.cell import Cell
from pivoter.selection import datafuncs as dfc
from pivoter.selection.base import Selectable
from tests.fixtures import fixture_simple_one_tab
from tests.unit.helpers import qcel, qcels


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_assert_quadrilaterals(selectable_simple1: Selectable):
    """
    Tests that we can assert a given list of cells
    represents a non sparse quadrilateral selection
    of cells
    """
    # Should not raise
    dfc.assert_quadrilaterals(selectable_simple1.excel_ref("A4:H17").cells)
    dfc.assert_quadrilaterals(selectable_simple1.excel_ref("G80:O80").cells)

    # Should raise
    with pytest.raises(AssertionError):
        is_quad = selectable_simple1.excel_ref("A4:H17")
        is_not_quad = is_quad - selectable_simple1.excel_ref("A4")
        dfc.assert_quadrilaterals(is_not_quad.cells)

    # Can return correct outlier indicies
    min_x, max_x, min_y, max_y = dfc.assert_quadrilaterals(
        selectable_simple1.excel_ref("A1:B4").cells, return_outlier_indicies=True
    )
    assert min_x == 0
    assert max_x == 1
    assert min_y == 0
    assert max_y == 3


def test_cell_is_within(selectable_simple1: Selectable):
    """
    Test that we can check for the presence of a cell with a
    list of cells.
    """

    @dataclass
    class Case:
        cell: Cell
        ref: str
        found: bool

    for case in [Case(qcel("A1"), "A1:A10", True), Case(qcel("A1"), "B1:B10", False)]:
        assert (
            dfc.cell_is_within(selectable_simple1.excel_ref(case.ref).cells, case.cell)
            == case.found
        ), f"Expected cell {case.cell} within {case.ref} to be {case.found}"


def test_matching_xy_cells(selectable_simple1: Selectable):
    """
    Test we can ask for and recieve specific cells from with a table
    """

    msg = "cannot find {} in {}"

    find = qcels("A2:A3")
    found: List[Cell] = dfc.matching_xy_cells(selectable_simple1.cells, find)
    assert len(found) == 2
    for cell in found:
        exp = ["A2val", "A3val"]
        assert cell.value in exp, msg.format(cell.value, exp)

    find = [qcel("D5"), qcel("I17")]  # D3 and H17
    found: List[Cell] = dfc.matching_xy_cells(selectable_simple1.cells, find)
    assert len(found) == 2
    for cell in found:
        exp = ["D5val", "I17val"]
        assert cell.value in exp, msg.format(cell.value, exp)
