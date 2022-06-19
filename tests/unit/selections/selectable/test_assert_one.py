import pytest

from pivotertesthelpers import single_table_test_input
from pivoter.models.source.cell import Cell
from pivoter.selection.base import Selectable


@pytest.fixture
def single_excel_input_A1() -> Selectable:
    """
    A single table input, one column of three cells for
    (in excel terms) A1:A3
    """
    return single_table_test_input(
        [
            Cell(x=0, y=0, value="foo"),
        ],
        "single fixture table 1"
    )


@pytest.fixture
def single_excel_input_A1A2() -> Selectable:
    """
    A single table input, one column of three cells for
    (in excel terms) A1:A3
    """
    return single_table_test_input(
        [
            Cell(x=0, y=0, value="foo"),
            Cell(x=0, y=1, value="bar")
        ],
        "single fixture table 2"
    )


def test_assert_one_with_single_cell(single_excel_input_A1: Selectable):
    """
    Test assert one behaves correctly on a selection consisting
    of one cell
    """
    single_excel_input_A1.assert_one()


def test_assert_one_without_single_cell(single_excel_input_A1A2: Selectable):
    """
    Test assert one behaves correctly on a selection not consisiting
    of a single cell.
    """
    
    with pytest.raises(AssertionError):
        single_excel_input_A1A2.assert_one()