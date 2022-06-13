import pytest

from helpers import single_table_input
from pivoter.models.source import Cell, Input
from pivoter.exceptions import IteratingSingleTableError


@pytest.fixture
def single_input_A1():
    """A single table input, one column of one cell"""
    return single_table_input([Cell(x=0, y=0, value="foo")], "single input A1",)

@pytest.fixture
def single_unnamed_input_A1():
    """A single table input, one column of one cell"""
    return single_table_input([Cell(x=0, y=0, value="foo")])


def test_cannot_iterate_single_table_inputs(single_input_A1: Input):
    """
    Confirm the appropriate error is raised where a user tries to
    iterate through an input consisting of exactly one input.
    """

    with pytest.raises(IteratingSingleTableError):
        for table in single_input_A1:
            ...


def test_table_name_property_returns_name(single_input_A1: Input):
    """
    If a table is named, confirm we can access the name
    property.
    """
    assert single_input_A1.name == "single input A1"


def test_table_title_property_returns_name(single_input_A1: Input):
    """
    If a table is named, confirm we can access the name
    property.
    """
    assert single_input_A1.title == "single input A1"


def test_table_name_property_returns_error():
    """
    If a table is not named, confirm accessing its name
    property returns the appropriate error.
    """
    ...


if __name__ == "__main__":
    pytest()
