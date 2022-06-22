from typing import List

from .helpers import single_table_test_input, multiple_table_test_input
from pivoter.models.source.cell import Cell
from pivoter.selection.base import Selectable


def single_input_multicells():
    """A single table input, two columns of one cell"""
    return single_table_test_input(
        [Cell(x=0, y=0, value="foo"), Cell(x=1, y=0, value="bar")]
    )


def single_unnamed_input_A1():
    """A single table input, one column of one cell"""
    return single_table_test_input([Cell(x=0, y=0, value="foo")])


def single_unnamed_input_B1():
    """A single table input, one column of one cell"""
    return single_table_test_input([Cell(x=1, y=0, value="bar")])


def two_cell_table_A1A2() -> Selectable:
    return single_table_test_input(
        [Cell(x=0, y=0, value="foo"), Cell(x=0, y=0, value="bar")]
    )


def multiple_input_A1() -> Selectable:
    """A multiple table input, one column of one cell"""
    return multiple_table_test_input(
        [
            [[Cell(x=0, y=0, value="foo in 1")], "single input A1 table 1"],
            [[Cell(x=0, y=0, value="foo in 2")], "single input A1 table 2"],
        ]
    )


def single_table_input_A1() -> Selectable:
    """
    A single table input, one column of three cells for
    (in excel terms) A1:A3
    """
    return single_table_test_input(
        [
            Cell(x=0, y=0, value="of A1"),
        ],
        "single fixture table 1",
    )


def single_excel_input_A1A2() -> Selectable:
    """
    A single table input, one column of three cells for
    (in excel terms) A1:A3
    """
    return single_table_test_input(
        [Cell(x=0, y=0, value="foo"), Cell(x=0, y=1, value="bar")],
        "single fixture table 2",
    )


def single_input_mixed_blank_and_not():
    """A single table input, one column of one cell"""
    return single_table_test_input(
        [
            Cell(x=0, y=0, value=""),
            Cell(x=0, y=1, value=" "),
            Cell(x=0, y=1, value="    "),
            Cell(x=0, y=1, value=None),
            Cell(x=1, y=0, value="foo"),
            Cell(x=1, y=1, value="bar"),
            Cell(x=1, y=1, value="baz"),
        ],
        "single input A1",
        Selectable,
    )


def single_input_A1F5() -> Selectable:
    """
    A single table input, in excel terms A1:F5
    """
    return single_table_test_input(
        [
            Cell(x=0, y=0, value="of A1"),
            Cell(x=0, y=1, value="of A2"),
            Cell(x=0, y=2, value="of A3"),
            Cell(x=0, y=3, value="of A4"),
            Cell(x=0, y=4, value="of A5"),
            Cell(x=1, y=0, value="of B1"),
            Cell(x=1, y=1, value="of B2"),
            Cell(x=1, y=2, value="of B3"),
            Cell(x=1, y=3, value="of B4"),
            Cell(x=1, y=4, value="of B5"),
            Cell(x=2, y=0, value="of C1"),
            Cell(x=2, y=1, value="of C2"),
            Cell(x=2, y=2, value="of C3"),
            Cell(x=2, y=3, value="of C4"),
            Cell(x=2, y=4, value="of C5"),
            Cell(x=3, y=0, value="of D1"),
            Cell(x=3, y=1, value="of D2"),
            Cell(x=3, y=2, value="of D3"),
            Cell(x=3, y=3, value="of D4"),
            Cell(x=3, y=4, value="of D5"),
            Cell(x=4, y=0, value="of E1"),
            Cell(x=4, y=1, value="of E2"),
            Cell(x=4, y=2, value="of E3"),
            Cell(x=4, y=3, value="of E4"),
            Cell(x=4, y=4, value="of E5"),
            Cell(x=5, y=0, value="of F1"),
            Cell(x=5, y=1, value="of F2"),
            Cell(x=5, y=2, value="of F3"),
            Cell(x=5, y=3, value="of F4"),
            Cell(x=5, y=4, value="of F5"),
        ],
        "single fixture table A1:F5",
    )
