from dataclasses import dataclass
from typing import List

import pytest

from datachef import datafuncs as dfc
from datachef.exceptions import BadExcelReferenceError, ReversedExcelRefError
from datachef.models.source.cell import BaseCell
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_assert_excel_ref_within_cells(selectable_simple1: Selectable):
    """
    Test we can assert the presence of a specific cell within a list
    if cells by passing it an excel reference.
    """

    s = selectable_simple1.excel_ref("F10:H25")
    dfc.assert_excel_ref_within_cells(s.cells, "H14")
    dfc.assert_excel_ref_within_cells(s.cells, "H20")
    dfc.assert_excel_ref_within_cells(s.cells, "G12")
    dfc.assert_excel_ref_within_cells(s.cells, "H24")
    dfc.assert_excel_ref_within_cells(s.cells, "F10")

    with pytest.raises(AssertionError):
        dfc.assert_excel_ref_within_cells(s.cells, "XX200")

    with pytest.raises(AssertionError):
        dfc.assert_excel_ref_within_cells(s.cells, "F26")


def test_any_excel_ref_as_wanted_basecells():
    """
    Confirm that any excel reference can correctly be converted to a
    list of BaseCells
    """

    @dataclass
    class Case:
        excel_ref: str
        cells: List[BaseCell]

    for case in [
        Case("A1:B1", [BaseCell(x=0, y=0), BaseCell(x=1, y=0)]),
        Case(
            "A2:C3",
            [
                BaseCell(x=0, y=1),
                BaseCell(x=0, y=2),
                BaseCell(x=1, y=1),
                BaseCell(x=1, y=2),
                BaseCell(x=2, y=1),
                BaseCell(x=2, y=2),
            ],
        ),
        Case("ZB1", [BaseCell(x=27, y=0)]),
    ]:

        cells: List[BaseCell] = dfc.any_excel_ref_as_wanted_basecells(case.excel_ref)

        assert len(cells) == len(case.cells), (
            "Excel ref resulting in unexpected number of cell references. "
            f"Got {len(cells)}, expecting {len()}"
        )

        for cell in cells:
            assert (
                cell in case.cells
            ), f"Cell {cell} missing from expected cells {case.cells}"

        for cell in case.cells:
            assert cell in cells, f"Cell {cell} missing from expected cells {cells}"

    # Confirm error raises for bad excel reference
    with pytest.raises(BadExcelReferenceError):
        dfc.any_excel_ref_as_wanted_basecells("foo")


def test_any_excel_ref_as_wanted_basecells():
    """
    Test that we can convert any excel reference into BaseCell(s) and
    that an appropriate error is raised for an invalid reference.
    """

    bcells: List[BaseCell] = dfc.any_excel_ref_as_wanted_basecells("B1:B2")
    assert len(bcells) == 2
    assert BaseCell(1, 0) in bcells
    assert BaseCell(1, 1) in bcells

    bcells: List[BaseCell] = dfc.any_excel_ref_as_wanted_basecells("G3")
    assert len(bcells) == 1
    assert BaseCell(6, 2) in bcells

    with pytest.raises(BadExcelReferenceError):
        dfc.any_excel_ref_as_wanted_basecells("3G")

    with pytest.raises(ReversedExcelRefError):
        dfc.any_excel_ref_as_wanted_basecells("C5:A1")


def test_single_excel_row_to_y_index(selectable_simple1: Selectable):
    """
    Confirm that passing in an excel reference consisting of a single
    row number exhbits the expected behaviour.
    """
    s = selectable_simple1.excel_ref("1")
    assert dfc.basecells_to_excel_ref(s.cells) == "A1:Z1"


def test_single_excel_column_to_x_index(selectable_simple1: Selectable):
    """
    Confirm that passing in an excel reference consisting of a column
    refernce in the form of letters exhbits the expected behaviour.
    """
    s = selectable_simple1.excel_ref("A")
    assert dfc.basecells_to_excel_ref(s.cells) == "A1:A100"
