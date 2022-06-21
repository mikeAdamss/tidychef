import pytest

from pivoter.models.source.cell import Cell
from pivoter.selection.base import Selectable
from pivotertesthelpers import single_table_test_input


@pytest.fixture
def single_input_mixed_blank_and_not():
    """A single table input, one column of one cell"""
    return single_table_test_input(
        [
            Cell(x=0, y=0, value=""),
            Cell(x=0, y=1, value=" "),
            Cell(x=0, y=1, value="    "),
            Cell(x=0, y=1, value=None),
            Cell(x=1, y=0, value="foo"),
            Cell(x=1, y=1, value="bar"),
            Cell(x=1, y=1, value="baz"),
        ],
        "single input A1",
        Selectable,
    )


def test_all_blanks_from_table(single_input_mixed_blank_and_not: Selectable):
    """
    Test that default blank behaviour filters to all expected cells.
    """
    single_input_mixed_blank_and_not.is_blank()
    assert len(single_input_mixed_blank_and_not.cells) == 4


def test_all_blanks_from_table_not_disregarding_whitespace(
    single_input_mixed_blank_and_not: Selectable,
):
    """
    Test that default blank behaviour filters to all expected cells.
    """
    single_input_mixed_blank_and_not.is_blank(disregard_whitespace=False)
    assert len(single_input_mixed_blank_and_not.cells) == 2


def test_all_non_blanks_from_table(single_input_mixed_blank_and_not: Selectable):
    """
    Test that default non blank behaviour filters to all expected cells.
    """
    single_input_mixed_blank_and_not.is_not_blank()
    assert len(single_input_mixed_blank_and_not.cells) == 3
