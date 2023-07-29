import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


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


def test_tables_have_expected_length(selectable_simple1: Selectable):
    """
    Test that tables return the expected len
    """

    assert len(selectable_simple1) == 2600
