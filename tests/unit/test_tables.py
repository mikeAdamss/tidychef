import pytest 

from helpers import single_table_input
from pivoter.models.source import Cell
from pivoter.exceptions import IteratingSingleTableError

@pytest.fixture
def single_input_1():
    """A single table input, one column of one cell"""
    return single_table_input("single fixture table 1", [Cell(x=0, y=0, value="foo")])


def test_cannot_iterate_single_table_inputs(single_input_1):
    """
    Confirm the appropriate error is raised where a user tries to
    iterate through an input consisting of exactly one input.
    """

    with pytest.raises(IteratingSingleTableError):
        for table in single_input_1:
            ...

if __name__ == "__main__":
    pytest()