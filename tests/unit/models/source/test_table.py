import pytest

from datachef.exceptions import InvalidTableSignatures, UnnamedTableError
from datachef.models.source.input import BaseInput
from datachef.models.source.table import LiveTable
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab, fixture_simple_two_tabs


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


@pytest.fixture
def selectable_of2_simple1():
    return fixture_simple_two_tabs()


def test_livetable_name_setter_and_getter(selectable_simple1: Selectable):
    """
    Test we can both set and retreive the name property as defined
    on the LiveTable class
    """

    selectable_simple1.name = "foo"
    assert selectable_simple1.name == "foo"


def test_livetable_name_getter_unnamed_table_err(
    selectable_simple1: Selectable,
):
    """
    Test the expected error is raised at the LiveTable class level if
    we try and access an unset name property.
    """

    with pytest.raises(UnnamedTableError):
        selectable_simple1.name


def test_livetable_with_unmatched_signatues_raises(
    selectable_of2_simple1: BaseInput,
):
    """
    Test that where we create a class:LiveTable from two tables with
    unmatching signatures the appropriate error is raised.
    """

    with pytest.raises(InvalidTableSignatures):
        LiveTable(
            selectable_of2_simple1.tables[0].pristine,
            selectable_of2_simple1.tables[1].pristine,
        )


def test_selectable_name_property_returns_name(selectable_of2_simple1: BaseInput):
    """
    If a table is named, confirm we can access the name
    property.
    """

    for tab in selectable_of2_simple1:
        assert "I am table 1" == tab.name or "I am table 2" == tab.name
