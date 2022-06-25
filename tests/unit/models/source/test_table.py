import pytest

from pivoter.exceptions import InvalidTableSignatures, UnnamedTableError
from pivoter.models.source.table import LiveTable
from pivoter.selection.base import Selectable
from tests.fixtures import fixture_simple_one_tab, fixture_simple_two_tabs


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


@pytest.fixture
def sheet_of_two_tables():
    return fixture_simple_two_tabs()


def test_livetable_name_setter_and_getter(table_simple_as_xls1: Selectable):
    """
    Test we can both set and retreive the name property as defined
    on the LiveTable class
    """

    ltable: LiveTable = table_simple_as_xls1.selected_table
    ltable.name = "foo"
    assert ltable.name == "foo"


def test_livetable_name_getter_unnamed_table_err(
    table_simple_as_xls1: Selectable,
):
    """
    Test the expected error is raised at the LiveTable class level if
    we try and access an unset name property.
    """

    ltable: LiveTable = table_simple_as_xls1.selected_table
    with pytest.raises(UnnamedTableError):
        ltable.name


def test_livetable_with_unmatched_signatues_raises(
    sheet_of_two_tables: Selectable,
):
    """
    Test that where we create a class:LiveTable from two tables with
    unmatching signatures the appropriate error is raised.
    """

    with pytest.raises(InvalidTableSignatures):
        LiveTable(
            sheet_of_two_tables.tables[0].pristine,
            sheet_of_two_tables.tables[1].pristine,
        )
