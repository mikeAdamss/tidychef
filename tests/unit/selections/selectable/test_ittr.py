import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.models.source.cell import Cell
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_conform_selection_iteration(selectable_simple1: Selectable):
    """
    Confirm that selection iterations works as expected
    """

    for cell in selectable_simple1:
        assert isinstance(cell, Cell)
