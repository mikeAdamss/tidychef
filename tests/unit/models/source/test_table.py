import copy
import pytest

from datachef.exceptions import InvalidTableSignatures, UnnamedTableError
from datachef.models.source.table import LiveTable, Table
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


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
    selectable_simple1: Selectable,
):
    """
    Test that where we create a class:LiveTable from two tables with
    unmatching signatures the appropriate error is raised.
    """

    table1 = Table(selectable_simple1.pcells)
    table2 = Table(selectable_simple1.pcells)
    
    with pytest.raises(InvalidTableSignatures):
        LiveTable(table1, table2)

def test_tables_have_expected_length(selectable_simple1: Selectable):
    """
    Test that tables return the expected len
    """

    assert len(selectable_simple1) == 2600
