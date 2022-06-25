from dataclasses import dataclass
from typing import List

import pytest

from pivoter.models.source.cell import BaseCell
from pivoter.selection.base import Selectable
from pivoter.utils import cellutils
from tests.fixtures import fixture_is_wide, fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


@pytest.fixture
def table_is_wide():
    return fixture_is_wide()


def test_excel_ref_to_x(table_is_wide: Selectable):
    """
    Given excel references, return an x co-ordinate
    """

    for excel_ref, expected_x in [
        ["A1", 0],
        ["AA1", 26],
    ]:
        got_x = table_is_wide.excel_ref(excel_ref).cells[0].x
        assert got_x == expected_x, f"Expected {expected_x}, got {got_x}"


def test_excel_row_to_y():
    """
    Test converting an excel row number into a y offset
    """
    assert cellutils.number_to_y(7) == 6


def test_y_to_excel_row():
    """
    Test converting an excel row number into a y offset
    """
    assert cellutils.y_to_number(6) == 7


def test_single_excel_ref(selectable_simple1: Selectable):
    """
    Given a single cell excel reference, return the correct
    BaseCell
    """

    for excel_ref, expected in [
        ["A1", BaseCell(0, 0)],
        ["C17", BaseCell(2, 16)],
    ]:
        assert selectable_simple1.excel_ref(excel_ref).cells[0].matches_xy(expected)


def test_x_to_letters():
    """
    Given an x co-ordinate, covert that co-ordinate to the
    excel letters represnting it as a column
    """

    @dataclass
    class Case:
        x: int
        expected: str

    for case in [Case(5, "F"), Case(26, "AA"), Case(25, "Z"), Case(51, "AZ")]:
        assert (
            cellutils.x_to_letters(case.x) == case.expected
        ), f"Expected {case.expected} from x:{case.x}, but got {cellutils.x_to_letters(case.x)}"


def test_excel_ref_to_basecells():
    """
    Confirm that excel references can correctly be converted to lists of BaseCells
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

        cells: List[BaseCell] = cellutils.excel_ref_as_wanted_basecells(case.excel_ref)

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
