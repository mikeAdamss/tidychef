"""
Tests relating to pivoters uderlying pivoter.models.source.BaseInput class
and its control of a users workflow.
"""

import copy
import pytest

from helpers import multiple_table_test_input, single_table_test_input
from pivoter.models.source.cell import Cell
from pivoter.models.source.input import BaseInput
from pivoter.exceptions import (
    IteratingSingleTableError,
    UnnamedTableError,
    UnalignedTableOperation
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

@pytest.fixture()
def single_input_multicells():
    """A single table input, two columns of one cell"""
    return single_table_test_input(
        [
            Cell(x=0, y=0, value="foo"),
            Cell(x=1, y=0, value="bar")
        ]
    )


@pytest.fixture
def single_unnamed_input_A1():
    """A single table input, one column of one cell"""
    return single_table_test_input([Cell(x=0, y=0, value="foo")])


@pytest.fixture
def single_unnamed_input_B1():
    """A single table input, one column of one cell"""
    return single_table_test_input([Cell(x=1, y=0, value="bar")])


def test_cannot_iterate_single_table_inputs(single_input_A1: BaseInput):
    """
    Confirm the appropriate error is raised where a user tries to
    iterate through an input consisting of exactly one table.
    """

    with pytest.raises(IteratingSingleTableError):
        for table in single_input_A1:
            """ never triggered """


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


def test_subtract_operator(single_input_multicells: BaseInput):
    """
    Test we try and make a substraction of cells from a table selection,
    using another selection taken from said table.
    """

    assert len(single_input_multicells.cells) == 2

    selection_to_remove = copy.deepcopy(single_input_multicells)
    selection_to_remove.cells = selection_to_remove.datamethods._cells_on_x_index(selection_to_remove.cells, 0)

    single_input_multicells = single_input_multicells - selection_to_remove
    assert len(single_input_multicells.cells) == 1


def test_subtract_operator_raises_for_unaligned_tables(single_unnamed_input_A1: BaseInput, single_unnamed_input_B1: BaseInput):
    """
    Test that a a suitable error is raised if we try and make a substraction of
    cells using selections taken from different tables.
    """

    with pytest.raises(UnalignedTableOperation):
        single_unnamed_input_A1 - single_unnamed_input_B1


