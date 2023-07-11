import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import pytest

from datachef.direction.directions import Direction, above, below, down, left, right, up
from datachef.exceptions import MissingLabelError
from datachef.lookup.engines.closest import Closest
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab
from tests.unit.helpers import qcel


@dataclass
class Result:
    ob_ref: Optional[str] = None
    resolved_ref: Optional[str] = None
    exception: Optional[Exception] = None


@dataclass
class Case:
    column_cells: List[str]
    direction: Direction
    expect_results: Optional[List[Result]] = None


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

    for case in [
        Case(
            column_cells=["B5", "G7", "L8", "J5", "H1", "R6", "Q2", "Z12"],
            direction=right,
            expect_results=[
                Result(ob_ref="A2", resolved_ref="B5"),
                Result(ob_ref="B2", resolved_ref="B5"),
                Result(ob_ref="C26", resolved_ref="G7"),
                Result(ob_ref="A2002", resolved_ref="B5"),
                Result(ob_ref="F100", resolved_ref="G7"),
                Result(ob_ref="G20", resolved_ref="G7"),
                Result(ob_ref="J20", resolved_ref="J5"),
                Result(ob_ref="H75", resolved_ref="H1"),
                Result(ob_ref="M2", resolved_ref="Q2"),
            ],
        )
    ]:

        # Select the specified cell(s)
        cells = selectable_simple_table.excel_ref(case.column_cells[0])
        if len(case.column_cells) > 1:
            for excel_ref in case.column_cells[1:]:
                cells = cells | selectable_simple_table.excel_ref(excel_ref)

        # Create the ranges
        closest_engine = Closest("", cells, case.direction)

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

                Direction was:
                --------------
                {closest_engine.direction}

                Lookup ranges were:
                -------------------
                {json.dumps(ranges_as_dict, indent=2)}
            """

            assert expected_result.resolved_ref == resulting_cell._excel_ref(), msg


def test_closest_left(selectable_simple_table: Selectable):
    """
    Test the closest engine can resolve visual left relationships
    as expected.
    """

    for case in [
        Case(
            column_cells=["B5", "G7", "L8", "J5", "H1", "R6", "Q2", "Z12"],
            direction=left,
            expect_results=[
                Result(ob_ref="C2", resolved_ref="B5"),
                Result(ob_ref="F7", resolved_ref="B5"),
                Result(ob_ref="G9", resolved_ref="G7"),
                Result(ob_ref="H2", resolved_ref="H1"),
                Result(ob_ref="K20", resolved_ref="J5"),
            ],
        )
    ]:

        # Select the specified cell(s)
        cells = selectable_simple_table.excel_ref(case.column_cells[0])
        if len(case.column_cells) > 1:
            for excel_ref in case.column_cells[1:]:
                cells = cells | selectable_simple_table.excel_ref(excel_ref)

        # Create the ranges
        closest_engine = Closest("", cells, case.direction)

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

                Direction was:
                --------------
                {closest_engine.direction}

                Lookup ranges were:
                -------------------
                {json.dumps(ranges_as_dict, indent=2)}
            """

            assert expected_result.resolved_ref == resulting_cell._excel_ref(), msg


def test_selectable_closest_wrapper_works(selectable_simple_table: Selectable):
    """
    Test that the selectable wrapper for Closest works as expected
    """
    assert isinstance(
        selectable_simple_table.excel_ref("A1")
        .label_as("foo")
        .finds_observations_closest(down),
        Closest,
    )

    # Constructor should raise if called on an unlabelled selection
    with pytest.raises(MissingLabelError):
        selectable_simple_table.excel_ref("A1").finds_observations_closest(down)
