"""
These tests are whoely concerned with testsing the dunder methods
controlling Input upon Input operators.
"""

import copy
import pytest

from helpers import single_table_test_input
from pivoter.models.source.cell import Cell
from pivoter.models.source.input import BaseInput
from pivoter.exceptions import UnalignedTableOperation


@pytest.fixture()
def single_input_multicells():
    """A single table input, two columns of one cell"""
    return single_table_test_input(
        [Cell(x=0, y=0, value="foo"), Cell(x=1, y=0, value="bar")]
    )


@pytest.fixture
def single_unnamed_input_A1():
    """A single table input, one column of one cell"""
    return single_table_test_input([Cell(x=0, y=0, value="foo")])


@pytest.fixture
def single_unnamed_input_B1():
    """A single table input, one column of one cell"""
    return single_table_test_input([Cell(x=1, y=0, value="bar")])


def test_sub_operator(single_input_multicells: BaseInput):
    """
    Test we try and make a substraction of cells from a table selection,
    using another selection taken from said table.
    """

    assert len(single_input_multicells.cells) == 2

    selection_to_remove = copy.deepcopy(single_input_multicells)
    selection_to_remove.cells = selection_to_remove.datamethods._cells_on_x_index(
        selection_to_remove.cells, 0
    )

    single_input_multicells = single_input_multicells - selection_to_remove
    assert len(single_input_multicells.cells) == 1


def test_subtract_operator_raises_for_unaligned_tables(
    single_unnamed_input_A1: BaseInput, single_unnamed_input_B1: BaseInput
):
    """
    Test that a a suitable error is raised if we try and make a substraction of
    cells using selections taken from different tables.
    """

    with pytest.raises(UnalignedTableOperation):
        single_unnamed_input_A1 - single_unnamed_input_B1
