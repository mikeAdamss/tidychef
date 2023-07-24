from dataclasses import dataclass
from typing import List

import pytest

from tidychef.models.source.cell import BaseCell
from tidychef.selection.selectable import Selectable
from tidychef.utils import cellutils
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
