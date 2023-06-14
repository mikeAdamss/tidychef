import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import pytest

from datachef.cardinal.directions import Direction, above, below, down, left, right, up
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

    ages = selectable_simple_table.excel_ref('B2') | selectable_simple_table.excel_ref('F2')
    engine = Within(ages, above, start=left(1), end=right(1))

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
        Case(ob_cell_ref="G3", resolved_cell_ref="F2")
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
        selectable_simple_table.excel_ref('B2') | 
        selectable_simple_table.excel_ref('D2') |
        selectable_simple_table.excel_ref('F2')
    )
    engine = Within(ages, above, start=right(1), end=left(1))

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
        Case(ob_cell_ref="G3", resolved_cell_ref="F2")
    ]:
        ob_cell = selectable_simple_table.excel_ref(case.ob_cell_ref)
        resolved_cell = engine.resolve(ob_cell.cells[0])
        assert case.resolved_cell_ref == resolved_cell._excel_ref()

        
