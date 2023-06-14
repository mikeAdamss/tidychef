import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import pytest

from datachef.cardinal.directions import Direction, above, below, down, left, right, up
from datachef.exceptions import AmbiguousLookupError, ImpossibleLookupError
from datachef.lookup.engines.closest import Closest
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


@dataclass
class Result:
    ob_ref: Optional[str] = None
    resolved_ref: Optional[str] = None
    exception: Optional[Exception] = None


@dataclass
class Case:
    column_cells: List[str]
    direction: Direction
    ob_ref: Optional[str] = None


def test_ambiguous_lookup_exception(selectable_simple_table: Selectable):
    """
    Test that an AmbiguousLookupError is raised where a user
    creates a closest relationship where 2 or more cells are
    equally valid.
    """

    for case in [
        Case(column_cells=["A1", "G1"], direction=up),
        Case(column_cells=["A1", "G1"], direction=down),
        Case(column_cells=["A1", "G1"], direction=above),
        Case(column_cells=["A1", "G1"], direction=below),
        Case(column_cells=["A1", "A10"], direction=left),
        Case(column_cells=["A1", "A10"], direction=right),
    ]:

        cells = selectable_simple_table.excel_ref(case.column_cells[0])
        if len(case.column_cells) > 1:
            for excel_ref in case.column_cells[1:]:
                cells = cells | selectable_simple_table.excel_ref(excel_ref)

        with pytest.raises(AmbiguousLookupError):
            Closest(case.direction, cells)


def test_out_of_bounds_exception(selectable_simple_table: Selectable):
    """
    Test that an OutOfBoundsError is raised where a user
    tries a lookup in a direction where no cells have been
    selected
    """
    for case in [
        Case(column_cells=["B5", "F6"], direction=up, ob_ref="B4"),
        Case(column_cells=["B5", "F6"], direction=down, ob_ref="F8"),
        Case(column_cells=["B5", "F6"], direction=left, ob_ref="A4"),
        Case(column_cells=["B5", "F6"], direction=right, ob_ref="G1"),
    ]:

        cells = selectable_simple_table.excel_ref(case.column_cells[0])
        if len(case.column_cells) > 1:
            for excel_ref in case.column_cells[1:]:
                cells = cells | selectable_simple_table.excel_ref(excel_ref)

        closest_engine = Closest(case.direction, cells)

        with pytest.raises(ImpossibleLookupError):
            query_cell = qcel(case.ob_ref)
            closest_engine.resolve(query_cell)
