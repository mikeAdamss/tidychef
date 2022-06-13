import pytest

from pivoter.models.source import Cell, LiveTable, Input
from helpers import single_table_input


@pytest.fixture
def single_input_1():
    """A single table input, one column of one cell"""
    return single_table_input("single fixture table 1", [Cell(x=0, y=0, value="foo")])


@pytest.fixture
def single_input_2():
    """A single table input, one column of three cells"""
    return single_table_input(
        "single fixture table 1",
        [
            Cell(x=0, y=0, value="foo"),
            Cell(x=0, y=1, value="bar"),
            Cell(x=0, y=2, value="baz"),
        ],
    )


def test_lone_value_selector(single_input_1: Input) -> LiveTable:
    """
    Test we can return the value for selections of exactly one cell
    """
    assert single_input_1.excel_ref("A1").lone_value() == "foo"


def tesst_lone_value_on_multiple_values_errors(single_input_2: Input) -> LiveTable:
    """
    Test than calling Input.long_value() on a filtered table containing
    more than one value raises.
    """
    ...


if __name__ == "__main__":
    pytest()
