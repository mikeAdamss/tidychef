import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import pytest

from datachef.cardinal.directions import Direction, above, below, down, left, right, up
from datachef.lookup.engines.closest import Closest
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from tests.unit.helpers import qcel
from tests.fixtures import fixture_simple_one_tab

@dataclass
class Result:
    ob_ref: Optional[str] = None
    resolved_ref:Optional[str] = None
    exception: Optional[Exception] = None

@dataclass
class Case:
    column_cells: List[str]
    direction: Direction
    expect_results: List[Result]


@pytest.fixture
def selectable_simple_table() -> Selectable:
    """
    Sample table, cells are based on excel ref

    A1 = "A1Val
    Z20 = "Z20Val"
    etc
    """
    return fixture_simple_one_tab()

def test_closest_right(selectable_simple_table: Selectable):
    """
    Test the closest engine can resolve visual right relationships
    as expected
    """

    for case in  [
        Case(
            column_cells=["B5", "G7"],
            direction=right,
            expect_results=[
                Result(ob_ref="A2",resolved_ref="B5"),
                Result(ob_ref="B2",resolved_ref="B5"),
                Result(ob_ref="A2002",resolved_ref="B5"),
                Result(ob_ref="F100",resolved_ref="G7"),
                Result(ob_ref="G20",resolved_ref="G7")
            ])
        ]:
        
        # Select the specified cell(s)
        cells = selectable_simple_table.excel_ref(case.column_cells[0])
        if len(case.column_cells) > 1:
            for excel_ref in case.column_cells[1:]:
                cells = cells | selectable_simple_table.excel_ref(excel_ref)

        # Create the ranges
        closest_engine = Closest(case.direction, cells)

        for expected_result in case.expect_results:

            ob_cell = qcel(expected_result.ob_ref)
            resulting_cell: Cell = closest_engine.resolve(ob_cell)

            ranges_as_dict: dict = closest_engine.ranges._as_dict()
            msg = f"""
                Observation cell was:
                ---------------------
                excel ref: {expected_result.ob_ref}
                query cell: {ob_cell} 

                Result was:
                -----------
                expected: {expected_result.resolved_ref}
                got: {resulting_cell._excel_ref()} from {resulting_cell}

                Lookup ranges were:
                -------------------
                {json.dumps(ranges_as_dict, indent=2)}
            """

            resulting_cell: Cell = closest_engine.resolve(ob_cell)
            assert expected_result.resolved_ref == resulting_cell._excel_ref(), msg
