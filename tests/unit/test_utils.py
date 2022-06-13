import pytest
from typing import List

from pivoter.utils import cellutils
from pivoter.models.source import BaseCell


def test_excel_ref_to_x():
    """
    Given excel references, return an x co-ordinate
    """

    for excel_ref, expected_x in [
        ["A", 0],
        ["AA", 26],
        ["AAA", 52],
        ["AB", 27],
        ["DFG", 58],
    ]:
        got: int = cellutils.letter_to_x(excel_ref)
        assert expected_x == got, f"Expected {expected_x}, got {got}"


def text_excel_row_to_y():
    """
    Test converting an excel row number into a y offset
    """
    assert cellutils.number_to_y(7) == 6


def test_single_excel_ref():
    """
    Given a single cell excel reference, return the correct
    BaseCell
    """

    for excel_ref, expected in [
        ["A1", BaseCell(0, 0)],
        ["C17", BaseCell(2, 16)],
        ["DFG200", BaseCell(58, 199)],
    ]:
        assert cellutils.single_excel_ref_to_basecells(excel_ref)[0] == expected


def test_multiple_excel_ref():
    """
    Given a single cell excel reference, return a list of the correct BaseCell's.
    """

    expected: List
    for excel_ref, expected in [
        ["A1:A2", [BaseCell(0, 0), BaseCell(0, 1)]]
    ]:
        cells_from_excel_ref: List[BaseCell] = cellutils.multi_excel_ref_to_basecells(excel_ref)
        msg = f'''
            Expected cells:
            {expected}

            Got Cells
            {cells_from_excel_ref}
            ''' 

        for ec in expected:
            assert ec in cells_from_excel_ref, msg
        assert len(expected) == len(cells_from_excel_ref), msg

if __name__ == "__main__":
    pytest()
