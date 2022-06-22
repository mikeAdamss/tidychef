from dis import dis
import pytest

from pivoter.exceptions import InvalidCellObjectError
from pivoter.selection.base import Selectable
from tests.fixtures import fixture_with_blanks

@pytest.fixture
def table_with_blanks():
    return fixture_with_blanks()


def test_all_blanks_from_table(table_with_blanks: Selectable):
    """
    Test that default blank behaviour filters to all expected cells.
    """
    assert len(table_with_blanks.cells) == 6
    just_blanks = table_with_blanks.is_blank()
    assert len(just_blanks.cells) == 3


def test_all_blanks_from_table_not_disregarding_whitespace(
    table_with_blanks: Selectable,
):
    """
    Test that default blank behaviour filters to all expected cells.
    """
    assert len(table_with_blanks.cells) == 6
    just_blanks = table_with_blanks.is_blank(disregard_whitespace=False)
    assert len(just_blanks.cells) == 1


def test_all_non_blanks_from_table(table_with_blanks: Selectable):
    """
    Test that default non blank behaviour filters to all expected cells.
    """
    table_with_blanks.is_not_blank()
    assert len(table_with_blanks.cells) == 3
