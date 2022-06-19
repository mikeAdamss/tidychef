"""
Tests relating to pivoters uderlying pivoter.models.source.BaseInput class
and its control of a users workflow.
"""

import pytest

from helpers import multiple_table_test_input, single_table_test_input
from pivoter.models.source.cell import Cell
from pivoter.models.source.input import BaseInput
from pivoter.exceptions import (
    IllegalOperationError,
    IteratingSingleTableError,
    UnnamedTableError,
)


@pytest.fixture
def single_input_A1():
    """A single table input, one column of one cell"""
    return single_table_test_input(
        [Cell(x=0, y=0, value="foo")],
        "single input A1",
    )


@pytest.fixture
def multiple_input_A1():
    """A multiple table input, one column of one cell"""
    return multiple_table_test_input(
        [
            [[Cell(x=0, y=0, value="foo in 1")], "single input A1 table 1"],
            [[Cell(x=0, y=0, value="foo in 2")], "single input A1 table 2"],
        ]
    )


@pytest.fixture
def single_unnamed_input_A1():
    """A single table input, one column of one cell"""
    return single_table_test_input([Cell(x=0, y=0, value="foo")])


def test_cannot_iterate_single_table_inputs(single_input_A1: BaseInput):
    """
    Confirm the appropriate error is raised where a user tries to
    iterate through an input consisting of exactly one table.
    """

    with pytest.raises(IteratingSingleTableError):
        for table in single_input_A1:
            ...


def test_can_iterate_multiple_table_inputs(multiple_input_A1: BaseInput):
    """
    Confirm the user can iterate through the tables in the expected
    manner.
    """

    for i, table in enumerate(multiple_input_A1):
        if i == 0:
            assert table.name == "single input A1 table 1"
        if i == 1:
            assert table.name == "single input A1 table 2"
        assert i == 0 or i == 1


def test_table_name_property_returns_name(single_input_A1: BaseInput):
    """
    If a table is named, confirm we can access the name
    property.
    """
    assert single_input_A1.name == "single input A1"


# Note: title as an alternate property acvessor for name is included
# for backwards compatibiity with the databaker library
def test_table_title_property_returns_name(single_input_A1: BaseInput):
    """
    If a table is named, confirm we can access the name
    via the alt property title.
    """
    assert single_input_A1.title == "single input A1"


def test_table_name_property_raises_err(single_unnamed_input_A1: BaseInput):
    """
    If a table is not named, confirm accessing its name
    property returns the appropriate error.
    """

    with pytest.raises(UnnamedTableError):
        single_unnamed_input_A1.name


def test_assign_to_pristine_cells_raises_err(single_unnamed_input_A1: BaseInput):
    """
    Make sure our defenseive programming around attempted
    assignments to the pristine copy of the cells making up
    a table (.pcells) is working as expected
    """

    with pytest.raises(IllegalOperationError):
        single_unnamed_input_A1.pcells = ""


if __name__ == "__main__":
    pytest()