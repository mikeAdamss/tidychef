from dataclasses import dataclass
from typing import List

import pytest

from tidychef import datafuncs as dfc
from tidychef.exceptions import CellsDoNotExistError
from tidychef.models.source.cell import BaseCell, Cell
from tidychef.selection.selectable import Selectable
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
        selectable_simple1.excel_ref("A1:B4").cells
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
    Test we can ask for and receive specific cells from with a table
    """

    msg = "cannot find {} in {}"

    find = qcels("A2:A3")
    found: List[Cell] = dfc.matching_xy_cells(selectable_simple1.cells, find)
    assert len(found) == 2
    for cell in found:
        exp = ["A2val", "A3val"]
        assert cell.value in exp, msg.format(cell.value, exp)

    find = [qcel("D5"), qcel("I17")]
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


def test_get_outlier_indicies(selectable_simple1: Selectable):
    """
    Test that when given a list of cell, we can get the outlier
    indicies.

    As in, the man and min x and y values in play.
    """

    cells = selectable_simple1.excel_ref("C4:F72").cells
    min_x, max_x, min_y, max_y = dfc.get_outlier_indicies(cells)
    assert min_x == 2
    assert max_x == 5
    assert min_y == 3
    assert max_y == 71

    cells = selectable_simple1.excel_ref("G46:L47").cells
    min_x, max_x, min_y, max_y = dfc.get_outlier_indicies(cells)
    assert min_x == 6
    assert max_x == 11
    assert min_y == 45
    assert max_y == 46

    cells = selectable_simple1.excel_ref("B7:F90").cells
    min_x, max_x, min_y, max_y = dfc.get_outlier_indicies(cells)
    assert min_x == 1
    assert max_x == 5
    assert min_y == 6
    assert max_y == 89


def test_matching_xy_cells(selectable_simple1: Selectable):
    """
    Where given two selections of cells, return all from the second
    list that are all present in the first.
    """

    cells: List[Cell] = selectable_simple1.excel_ref("F6:H10").cells
    wanted_cells: List[Cell] = selectable_simple1.excel_ref("F6:J10").cells
    found: List[Cell] = dfc.matching_xy_cells(cells, wanted_cells)
    assert len(found) == 15


def test_matching_xy_cell(selectable_simple1: Selectable):
    """
    Test we can select a specific Cell from a list of cells.
    """

    @dataclass
    class Case:
        ref: str
        wanted: str

    for case in [Case("A6:G19", "F8"), Case("B5:Z90", "X33"), Case("F46:G50", "G50")]:

        cells: List[Cell] = selectable_simple1.excel_ref(case.ref).cells
        cell: Cell = dfc.exactly_matching_xy_cell(cells, qcel(case.wanted))
        found_cell_ref: str = dfc.basecell_to_excel_ref(cell)
        assert (
            found_cell_ref == case.wanted
        ), f"Expecting {case.wanted}, from {case.ref}, got {found_cell_ref}"


def test_offsets(selectable_simple1: Selectable):
    """
    Tests for:

    minimum_x_offset
    maximum_x_offset
    minimum_y_offset
    maximum_y_offset
    """
    cells: List[Cell] = selectable_simple1.excel_ref("D16:Z77").cells
    assert dfc.minimum_x_offset(cells) == 3
    assert dfc.maximum_x_offset(cells) == 25
    assert dfc.minimum_y_offset(cells) == 15
    assert dfc.maximum_y_offset(cells) == 76


def test_specific_cell_from_xy(selectable_simple1: Selectable):
    """
    Confirm we can use an x and y co-ordinate to get a single cell
    from a list of cells.
    """

    cells: List[Cell] = selectable_simple1.excel_ref("D5:G67").cells

    cell: Cell = dfc.specific_cell_from_xy(cells, 3, 9)
    assert dfc.basecell_to_excel_ref(cell) == "D10"

    cell: Cell = dfc.specific_cell_from_xy(cells, 5, 63)
    assert dfc.basecell_to_excel_ref(cell) == "F64"

    cell: Cell = dfc.specific_cell_from_xy(cells, 4, 50)
    assert dfc.basecell_to_excel_ref(cell) == "E51"


def test_xycells_to_excel_ref(selectable_simple1: Selectable):
    """
    Test that where we are provided a list of selected cells
    representing an multicell excel reference:

    (a) it is a quadrilateral selection (because it has to be)
    (b) we can derrive the correctly expressed excel reference
    from it.
    """

    for ref in ["D5:G67", "A1:Z89", "J26:Q28"]:

        cells: List[Cell] = selectable_simple1.excel_ref(ref).cells
        assert dfc.basecells_to_excel_ref(cells) == ref

    # Check we raise for a non quadrilateral selection
    with pytest.raises(AssertionError):
        selection: Selectable = selectable_simple1.excel_ref("A1:D10")
        selection: Selectable = selection | selectable_simple1.excel_ref("Z8")
        dfc.basecells_to_excel_ref(selection.cells)


def test_all_used_x_indicies(selectable_simple1: Selectable):
    """
    Confirm we can get all unique x indicies within use in
    a list of cells
    """

    s = selectable_simple1.excel_ref("D5:F15")
    x_indicies: List[int] = dfc.all_used_x_indicies(s.cells)
    assert set(x_indicies) == {3, 4, 5}


def test_all_used_y_indicies(selectable_simple1: Selectable):
    """
    Confirm we can get all unique y indicies within use in
    a list of cells
    """

    s = selectable_simple1.excel_ref("D5:F15")
    x_indicies: List[int] = dfc.all_used_y_indicies(s.cells)
    assert set(x_indicies) == {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}
