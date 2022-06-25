from dataclasses import dataclass
from typing import List

import pytest

from pivoter.exceptions import CellsDoNotExistError
from pivoter.models.source.cell import BaseCell, Cell
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
        cell: BaseCell
        ref: str
        found: bool

    for case in [Case(qcel("A1"), "A1:A10", True), Case(qcel("A1"), "B1:B10", False)]:
        assert (
            dfc.cell_is_within(selectable_simple1.excel_ref(case.ref).cells, case.cell)
            == case.found
        ), f"Expected cell {case.cell} within {case.ref} to be {case.found}"


def test_cell_is_not_in(selectable_simple1: Selectable):
    """
    Test that we can check for the absense of a cell with a
    list of cells.
    """

    @dataclass
    class Case:
        cell: BaseCell
        ref: str
        found: bool

    for case in [Case(qcel("A1"), "A1:A10", False), Case(qcel("A1"), "B1:B10", True)]:
        assert (
            dfc.cell_is_not_within(
                selectable_simple1.excel_ref(case.ref).cells, case.cell
            )
            == case.found
        ), f"Expected cell {case.cell} within {case.ref} to be {case.found}"


def test_cells_not_in(selectable_simple1: Selectable):
    """
    Test we can get a list of cells from one list that are
    not included in a second list.
    """

    @dataclass
    class Case:
        cells_ref: str
        ref: str
        expected_count: int

    for case in [
        Case("A1:F1", "A1:E1", 1),
        Case("F20:G32", "F20:F32", 13),
        Case("C4:E6", "C4:E5", 3),
    ]:
        cells = qcels(case.cells_ref)
        cells_not_in: List[Cell] = dfc.cells_not_in(
            cells, selectable_simple1.excel_ref(case.ref).cells
        )
        assert (
            len(cells_not_in) == case.expected_count
        ), f"Cells from {case.cells_ref} not in {case.ref} should be {case.expected_count}, but got {len(cells_not_in)}"


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


def test_cells_on_x_index(selectable_simple1: Selectable):
    """
    Test we can use x indicides to select all cells for that column
    in a given selection of cells
    """

    @dataclass
    class Case:
        ref: str
        x: int
        expected: int

    for case in [Case("A1:F6", 3, 6), Case("G12:G56", 6, 45), Case("A1:F6", 9, 0)]:
        s: List[Cell] = selectable_simple1.excel_ref(case.ref).cells
        cells_on_index: List[Cell] = dfc.cells_on_x_index(s, case.x)
        assert (
            len(cells_on_index) == case.expected
        ), f"X axis {case.x} from cells {case.ref} should return {case.expected} cells, but got {len(cells_on_index)}"


def test_cells_on_y_index(selectable_simple1: Selectable):
    """
    Test we can use y indicides to select all cells for that row
    in a given selection of cells
    """

    @dataclass
    class Case:
        ref: str
        y: int
        expected: int

    for case in [Case("A1:F6", 3, 6), Case("G2:H56", 6, 2), Case("A1:F6", 3, 6)]:
        s: List[Cell] = selectable_simple1.excel_ref(case.ref).cells
        cells_on_index: List[Cell] = dfc.cells_on_y_index(s, case.y)
        assert (
            len(cells_on_index) == case.expected
        ), f"Y axis {case.y} from cells {case.ref} should return {case.expected} cells, but got {len(cells_on_index)}"


def test_ensure_human_read_order():
    """
    Given an unordered list of cells, return them in a human readable
    order.

    i.e top row to bottom row, left to right
    """

    cells = [
        BaseCell(5, 2),
        BaseCell(12, 12),
        BaseCell(2, 5),
        BaseCell(6, 2),
        BaseCell(3, 16),
        BaseCell(0, 0),
    ]
    ordered = dfc.ensure_human_read_order(cells)
    assert (
        str(ordered)
        == "[BaseCell(x=0, y=0), BaseCell(x=5, y=2), BaseCell(x=6, y=2), BaseCell(x=2, y=5), BaseCell(x=12, y=12), BaseCell(x=3, y=16)]"
    )


def test_exactly_matched_xy_cells(selectable_simple1: Selectable):
    """
    Test that:

    Exactly matching cells can be extracted from a selection.

    An error is raised where the requested cells are absent from
    the intial selection.
    """

    # Should work
    cells_ref = "G5:H8"
    wanted_cells_ref = "G6:H7"
    cells = selectable_simple1.excel_ref(cells_ref).cells
    wanted_cells: List[Cell] = selectable_simple1.excel_ref(wanted_cells_ref).cells
    found = dfc.exactly_matched_xy_cells(cells, wanted_cells)
    assert (
        len(found) == 4
    ), f"Expected 4 cells exactly matching {wanted_cells_ref} from {cells_ref}, got {len(found)}"

    # Should raise
    cells_ref = "G5:H8"
    wanted_cells_ref = "Z6:Z8"
    cells = selectable_simple1.excel_ref(cells_ref).cells
    wanted_cells: List[Cell] = selectable_simple1.excel_ref(wanted_cells_ref).cells
    with pytest.raises(CellsDoNotExistError):
        dfc.exactly_matched_xy_cells(cells, wanted_cells)
