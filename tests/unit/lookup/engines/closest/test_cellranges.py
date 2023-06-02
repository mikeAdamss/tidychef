import json
from dataclasses import dataclass
from typing import List

import pytest

from datachef.cardinal.directions import Direction, above, below, down, left, right, up
from datachef.lookup.engines.closest import CellRanges
from datachef.selection.selectable import Selectable
from tests.fixtures import (
    fixture_simple_band_tab,
    fixture_simple_one_tab,
    fixture_wide_band_tab,
    path_to_fixture,
)


@pytest.fixture
def selectable_simple_table() -> Selectable:
    """
    Sample table, cells are based on excel ref

    A1 = "A1Val
    Z20 = "Z20-Val"
    etc
    """
    return fixture_simple_one_tab()


@pytest.fixture
def selectable_simple_band_tab() -> Selectable:
    """
    Sample data, simple band table
    """
    return fixture_simple_band_tab()


@pytest.fixture
def selectable_wide_band_tab() -> Selectable:
    """
    Sample data, wide band table
    """
    return fixture_wide_band_tab()


def assert_breakpoints_as_dict_matches(
    cells: Selectable,
    cell_ranges: CellRanges,
    fixture: str,
    dictionary_expected,
    dictionary_got,
):
    """
    Helper to check that a dictionary of breakpoints
    taken from a CellRanges class matches an expected
    dictionary.
    """

    display = f"""

    failure for CellRanges
    ----------------------
    with direction: {cell_ranges.direction.name}
    from cells: {cells}
    using fixture: {fixture}
    
    dictionary_expected:
    ---------------
    {json.dumps(dictionary_expected, indent=2, default=lambda x: str(x))}
    
    dictionary_got:
    --------------------
    {json.dumps(dictionary_got, indent=2, default=lambda x: str(x))}
    """

    assert len(dictionary_expected) == len(
        dictionary_got
    ), f"Dictionaries have different lengths. {display}"
    for expected_principle_key, expected_principle_value in dictionary_expected.items():
        assert (
            expected_principle_key in dictionary_got.keys()
        ), f"Missing dictionary key {expected_principle_key}. {display}"

        for expected_sub_key, expected_sub_value in expected_principle_value.items():

            assert (
                expected_sub_key in dictionary_got[expected_principle_key].keys()
            ), f"Field {expected_sub_key} from dictionary_expected is not in dictionary_got. {display}"

            assert (
                expected_sub_value
                == dictionary_got[expected_principle_key][expected_sub_key]
            ), f"Value {expected_sub_value} from dictionary_expected is not in dictionary_got. {display}"


def test_cell_ranges(
    selectable_simple_band_tab: Selectable,
    selectable_wide_band_tab: Selectable,
    selectable_simple_table: Selectable,
):
    """
    Test the CellRanges constructor constructs ranges correctly
    """

    cells = selectable_simple_band_tab.excel_ref("A3").is_not_blank()
    cell_ranges = CellRanges(cells, up)

    @dataclass
    class Case:
        description: str
        excel_cells: List[str]
        selectable: Selectable
        json_fixture: str
        direction: Direction

    for case in [
        Case(
            description="Band tab, 'up' vertical range to A3",
            excel_cells=["A3"],
            selectable=selectable_simple_band_tab,
            json_fixture="band_upwards_A3.json",
            direction=up,
        ),
        Case(
            description="Band tab, 'above' vertical range to A3",
            excel_cells=["A3"],
            selectable=selectable_simple_band_tab,
            json_fixture="band_upwards_A3.json",
            direction=above,
        ),
        Case(
            description="Band tab, 'down' vertical range to A3",
            excel_cells=["A3"],
            selectable=selectable_simple_band_tab,
            json_fixture="band_downwards_A3.json",
            direction=down,
        ),
        Case(
            description="Band tab, 'below' vertical range to A3",
            excel_cells=["A3"],
            selectable=selectable_simple_band_tab,
            json_fixture="band_downwards_A3.json",
            direction=below,
        ),
        Case(
            description="Band tab wide, 'left' horizontal range to A3, G3",
            excel_cells=["A3", "G3"],
            selectable=selectable_wide_band_tab,
            json_fixture="band_left_A3_G3.json",
            direction=left,
        ),
        Case(
            description="Band tab wide, 'left' horizontal range to B3, G3",
            excel_cells=["B3", "G3"],
            selectable=selectable_wide_band_tab,
            json_fixture="band_left_B3_G3.json",
            direction=left,
        ),
        Case(
            description="Simple tab, 'left' horizontal range to F6, W2",
            excel_cells=["F6", "W2"],
            selectable=selectable_simple_table,
            json_fixture="simple_left_F6_W2.json",
            direction=left,
        ),
        Case(
            description="Simple tab, 'right' horizontal range to F6, W2",
            excel_cells=["F6", "W2"],
            selectable=selectable_simple_table,
            json_fixture="simple_right_F6_W2.json",
            direction=right,
        ),
    ]:

        # Select the specified cell(s)
        my_cells = case.selectable.excel_ref(case.excel_cells[0])
        if len(case.excel_cells) > 1:
            for excel_ref in case.excel_cells[1:]:
                my_cells = my_cells | case.selectable.excel_ref(excel_ref)

        # Create the ranges
        cell_ranges = CellRanges(my_cells, case.direction)

        # Open the fixture
        with open(path_to_fixture("json/closest", case.json_fixture)) as f:
            json_fixture = json.loads(f.read())

        # Compare CellRanges with json fixture representing the cell ranges.
        assert_breakpoints_as_dict_matches(
            my_cells,
            cell_ranges,
            case.json_fixture,
            json_fixture,
            cell_ranges._as_dict(),
        )
