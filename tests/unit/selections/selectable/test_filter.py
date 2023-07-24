from dataclasses import dataclass

import pytest

from tidychef import datafuncs as dfc
from tidychef.models.source.cell import Cell
from tidychef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_filter_with_lambda(selectable_simple1: Selectable):
    """
    Confirm that we can filter by passing a lambda function
    """

    s = selectable_simple1.excel_ref("A1:B12")
    assert len(s.cells) == 24
    s = s.filter(lambda cell: "A" in cell.value)
    assert len(s.cells) == 12
    assert dfc.basecells_to_excel_ref(s.cells) == "A1:A12"


def test_filter_with_class(selectable_simple1: Selectable):
    """
    Confirm that we can filter by passing in a function
    """

    def contains_a(cell: Cell):
        """
        Example function filter.
        True is the value of the cell contains "A"
        """
        return "A" in cell.value

    s = selectable_simple1.excel_ref("A1:B12")
    assert len(s.cells) == 24
    s = s.filter(contains_a)
    assert len(s.cells) == 12
    assert dfc.basecells_to_excel_ref(s.cells) == "A1:A12"


def test_filter_with_function(selectable_simple1: Selectable):
    """
    Confirm that we can filter by passing in a callable class
    """

    @dataclass
    class ContainsSpecificLetter:
        """
        Filter class to look for cells containing
        the specific letter
        """

        letter: str

        def __call__(self, cell: Cell):
            return self.letter in cell.value

    s = selectable_simple1.excel_ref("A1:B12")
    assert len(s.cells) == 24
    s = s.filter(ContainsSpecificLetter("A"))
    assert len(s.cells) == 12
    assert dfc.basecells_to_excel_ref(s.cells) == "A1:A12"
