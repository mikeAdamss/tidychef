import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import pytest

from datachef.cardinal.directions import Direction, above, below, down, left, right, up
from datachef.exceptions import ImpossibleLookupError, WithinAxisDeclarationError
from datachef.lookup.engines.within import Within
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab
from tests.unit.helpers import qcel


@pytest.fixture
def selectable_simple_table() -> Selectable:
    """
    Sample table, cells are based on excel ref

    A1 = "A1Val
    Z20 = "Z20Val"
    etc
    """
    return fixture_simple_one_tab()


def test_within_direction_up_traversal_leftright(selectable_simple_table: Selectable):
    """
    Simple sanity check of a within lookup

       |  A   |  B   |  C   |  D   |  E   |  F   |  G   |
    1  |      |      |      |      |      |      |      |
    2  |      | age1 |      |      |      | age2 |      |
    3  | ob1  | ob2  | ob3  |      | ob4  | ob5  | ob6  |
    """

    ages = selectable_simple_table.excel_ref("B2") | selectable_simple_table.excel_ref(
        "F2"
    )
    engine = Within("", ages, above, start=left(1), end=right(1))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="A3", resolved_cell_ref="B2"),
        Case(ob_cell_ref="B3", resolved_cell_ref="B2"),
        Case(ob_cell_ref="C3", resolved_cell_ref="B2"),
        Case(ob_cell_ref="E3", resolved_cell_ref="F2"),
        Case(ob_cell_ref="F3", resolved_cell_ref="F2"),
        Case(ob_cell_ref="G3", resolved_cell_ref="F2"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_within_direction_up_traversal_rightleft(selectable_simple_table: Selectable):
    """
    Simple sanity check of a within lookup

       |  A   |  B   |  C   |  D   |  E   |  F   |  G   |
    1  |      |      |      |      |      |      |      |
    2  |      | age1 |      | age2 |      | age2 |      |
    3  | ob1  | ob2  | ob3  |      | ob4  | ob5  | ob6  |
    """

    ages = (
        selectable_simple_table.excel_ref("B2")
        | selectable_simple_table.excel_ref("D2")
        | selectable_simple_table.excel_ref("F2")
    )
    engine = Within("", ages, above, start=right(1), end=left(1))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="A3", resolved_cell_ref="B2"),
        Case(ob_cell_ref="B3", resolved_cell_ref="B2"),
        Case(ob_cell_ref="C3", resolved_cell_ref="D2"),
        Case(ob_cell_ref="E3", resolved_cell_ref="F2"),
        Case(ob_cell_ref="F3", resolved_cell_ref="F2"),
        Case(ob_cell_ref="G3", resolved_cell_ref="F2"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_within_direction_down_traversal_rightleft(selectable_simple_table: Selectable):
    """
    Simple sanity check of a within lookup

       |  A   |  B   |  C   |  D   |  E   |  F   |  G   |
    2  |      |      |      |      |      |      |      |
    3  | ob1  | ob2  | ob3  |      | ob4  | ob5  | ob6  |
    4  |      | age1 |      | age2 |      |      | age3 |
    """

    ages = (
        selectable_simple_table.excel_ref("B4")
        | selectable_simple_table.excel_ref("D4")
        | selectable_simple_table.excel_ref("G4")
    )
    engine = Within("", ages, below, start=right(1), end=left(1))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="A3", resolved_cell_ref="B4"),
        Case(ob_cell_ref="B3", resolved_cell_ref="B4"),
        Case(ob_cell_ref="C3", resolved_cell_ref="D4"),
        Case(ob_cell_ref="E3", resolved_cell_ref="D4"),
        Case(ob_cell_ref="F3", resolved_cell_ref="G4"),
        Case(ob_cell_ref="G3", resolved_cell_ref="G4"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_within_direction_down_traversal_leftright(selectable_simple_table: Selectable):
    """
    Simple sanity check of a within lookup

       |  A   |  B   |  C   |  D   |  E   |  F   |  G   |
    2  |      |      |      |      |      |      |      |
    3  | ob1  | ob2  | ob3  |      | ob4  | ob5  | ob6  |
    4  |      | age1 |      | age2 |      |      | age3 |
    """

    ages = (
        selectable_simple_table.excel_ref("B4")
        | selectable_simple_table.excel_ref("D4")
        | selectable_simple_table.excel_ref("G4")
    )
    engine = Within("", ages, below, start=left(1), end=right(1))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="A3", resolved_cell_ref="B4"),
        Case(ob_cell_ref="B3", resolved_cell_ref="B4"),
        Case(ob_cell_ref="C3", resolved_cell_ref="B4"),
        Case(ob_cell_ref="E3", resolved_cell_ref="D4"),
        Case(ob_cell_ref="F3", resolved_cell_ref="G4"),
        Case(ob_cell_ref="G3", resolved_cell_ref="G4"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_within_direction_left_traversal_downup(selectable_simple_table: Selectable):
    """
    Simple sanity check of a within lookup

       |  A   |  B  |  C   |  D   |  E   |
    2  |      |     |      |      |      |
    3  |      | ob4 |      |      | ob8  |
    4  |      | ob3 |      |      | ob7  |
    5  | age1 | ob2 |      | age2 | ob6  |
    6  |      | ob1 |      |      | ob5  |
    """

    ages = selectable_simple_table.excel_ref("A5") | selectable_simple_table.excel_ref(
        "D5"
    )
    engine = Within("", ages, left, start=down(2), end=up(1))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="B3", resolved_cell_ref="A5"),
        Case(ob_cell_ref="B4", resolved_cell_ref="A5"),
        Case(ob_cell_ref="B5", resolved_cell_ref="A5"),
        Case(ob_cell_ref="B6", resolved_cell_ref="A5"),
        Case(ob_cell_ref="E3", resolved_cell_ref="D5"),
        Case(ob_cell_ref="E4", resolved_cell_ref="D5"),
        Case(ob_cell_ref="E5", resolved_cell_ref="D5"),
        Case(ob_cell_ref="E6", resolved_cell_ref="D5"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_within_direction_right_traversal_downup(selectable_simple_table: Selectable):
    """
    Simple sanity check of a within lookup

       |  A   |  B  |  C   |  D   |  E   |  F   |
    2  |      |     |      |      |      |      |
    3  |      | ob4 |      |      | ob8  | age3 |
    4  |      | ob3 |      |      | ob7  |      |
    5  |      | ob2 | age1 |      | ob6  |      |
    6  |      | ob1 |      |      | ob5  |      |
    """

    ages = selectable_simple_table.excel_ref("C5") | selectable_simple_table.excel_ref(
        "F3"
    )
    engine = Within("", ages, right, start=down(2), end=up(3))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="B3", resolved_cell_ref="C5"),
        Case(ob_cell_ref="B4", resolved_cell_ref="C5"),
        Case(ob_cell_ref="B5", resolved_cell_ref="C5"),
        Case(ob_cell_ref="B6", resolved_cell_ref="C5"),
        Case(ob_cell_ref="E3", resolved_cell_ref="F3"),
        Case(ob_cell_ref="E4", resolved_cell_ref="F3"),
        Case(ob_cell_ref="E5", resolved_cell_ref="F3"),
        Case(ob_cell_ref="E6", resolved_cell_ref="F3"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_within_direction_left_traversal_updown(selectable_simple_table: Selectable):
    """
     Simple sanity check of a within lookup

        |  A   |  B  |  C   |  D   |  E   |
     2  |      |     |      |      |      |
     3  |      | ob4 |      |      | ob8  |
     4  |      | ob3 |      | age2 | ob7  |
     5  | age1 | ob2 |      |      | ob6  |
     6  |      | ob1 |      |      | ob5  |
     7  |      |     |      |      |      |
     8  |      |     |      |      |      |
     9  |      | ob4 |      | age4 | ob8  |
    10  |      | ob3 |      |      | ob7  |
    11  |      | ob2 |      |      | ob6  |
    12  | age3 | ob1 |      |      | ob5  |
    13  |      |     |      |      |      |
    """

    ages = (
        selectable_simple_table.excel_ref("A5")
        | selectable_simple_table.excel_ref("A12")
        | selectable_simple_table.excel_ref("D4")
        | selectable_simple_table.excel_ref("D9")
    )
    engine = Within("", ages, left, start=up(3), end=down(3))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="B3", resolved_cell_ref="A5"),
        Case(ob_cell_ref="B4", resolved_cell_ref="A5"),
        Case(ob_cell_ref="B5", resolved_cell_ref="A5"),
        Case(ob_cell_ref="B6", resolved_cell_ref="A5"),
        Case(ob_cell_ref="E3", resolved_cell_ref="D4"),
        Case(ob_cell_ref="E4", resolved_cell_ref="D4"),
        Case(ob_cell_ref="E5", resolved_cell_ref="D4"),
        Case(ob_cell_ref="E6", resolved_cell_ref="D4"),
        Case(ob_cell_ref="B9", resolved_cell_ref="A12"),
        Case(ob_cell_ref="B10", resolved_cell_ref="A12"),
        Case(ob_cell_ref="B11", resolved_cell_ref="A12"),
        Case(ob_cell_ref="B12", resolved_cell_ref="A12"),
        Case(ob_cell_ref="E9", resolved_cell_ref="D9"),
        Case(ob_cell_ref="E10", resolved_cell_ref="D9"),
        Case(ob_cell_ref="E11", resolved_cell_ref="D9"),
        Case(ob_cell_ref="E12", resolved_cell_ref="D9"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_within_direction_right_traversal_updown(selectable_simple_table: Selectable):
    """
     Simple sanity check of a within lookup

        |  A   |  B  |  C   |  D   |  E   |  F   |
     2  |      |     |      |      |      |      |
     3  |      | ob4 |      |      | ob8  |      |
     4  |      | ob3 |      |      | ob7  | age2 |
     5  |      | ob2 | age1 |      | ob6  |      |
     6  |      | ob1 |      |      | ob5  |      |
     7  |      |     |      |      |      |      |
     8  |      |     |      |      |      |      |
     9  |      | ob4 |      |      | ob8  | age4 |
    10  |      | ob3 |      |      | ob7  |      |
    11  |      | ob2 |      |      | ob6  |      |
    12  |      | ob1 | age3 |      | ob5  |      |
    13  |      |     |      |      |      |      |
    """

    ages = (
        selectable_simple_table.excel_ref("C5")
        | selectable_simple_table.excel_ref("C12")
        | selectable_simple_table.excel_ref("F4")
        | selectable_simple_table.excel_ref("F9")
    )
    engine = Within("", ages, right, start=up(3), end=down(3))

    @dataclass
    class Case:
        ob_cell_ref: str
        resolved_cell_ref: str

    for case in [
        Case(ob_cell_ref="B3", resolved_cell_ref="C5"),
        Case(ob_cell_ref="B4", resolved_cell_ref="C5"),
        Case(ob_cell_ref="B5", resolved_cell_ref="C5"),
        Case(ob_cell_ref="B6", resolved_cell_ref="C5"),
        Case(ob_cell_ref="E3", resolved_cell_ref="F4"),
        Case(ob_cell_ref="E4", resolved_cell_ref="F4"),
        Case(ob_cell_ref="E5", resolved_cell_ref="F4"),
        Case(ob_cell_ref="E6", resolved_cell_ref="F4"),
        Case(ob_cell_ref="B9", resolved_cell_ref="C12"),
        Case(ob_cell_ref="B10", resolved_cell_ref="C12"),
        Case(ob_cell_ref="B11", resolved_cell_ref="C12"),
        Case(ob_cell_ref="B12", resolved_cell_ref="C12"),
        Case(ob_cell_ref="E9", resolved_cell_ref="F9"),
        Case(ob_cell_ref="E10", resolved_cell_ref="F9"),
        Case(ob_cell_ref="E11", resolved_cell_ref="F9"),
        Case(ob_cell_ref="E12", resolved_cell_ref="F9"),
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()


def test_axis_declaration_error():
    """
    Confirm that passing in invalid combinations of directions
    raises the expected error
    """
    with pytest.raises(WithinAxisDeclarationError):
        Within("", [], up, left(1), up(1))


def test_impossible_lookup_error(selectable_simple_table: Selectable):
    """
    Test that we correctly inform the user where they specify
    a lookup that is impossible.

    Simple sanity check of a within lookup

       |  A   |  B  |  C  |
    4  |      |     |     |
    5  | age1 | ob2 |     |
    6  |      |     |     |
    """

    ages = selectable_simple_table.excel_ref("A5")

    # Looking RIGHT for ages column header - where there's no selected cells
    engine = Within("", ages, right, start=down(2), end=up(1))

    with pytest.raises(ImpossibleLookupError):
        ob_cell = selectable_simple_table.excel_ref("B5")
        engine.resolve(ob_cell.cells[0])
