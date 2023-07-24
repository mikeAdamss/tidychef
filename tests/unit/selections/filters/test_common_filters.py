import pytest

from tidychef import datafuncs as dfc
from tidychef.selection import filters
from tidychef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab, fixture_vertical_dimensions


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


@pytest.fixture
def selectable_vertical_dimensions():
    return fixture_vertical_dimensions()


def test_filter_contains_string(selectable_simple1: Selectable):
    """
    Test the contains_string filter behaves as expected
    """

    s = selectable_simple1.excel_ref("A1:G25").filter(filters.contains_string("A"))
    assert len(s.cells) == 25
    assert dfc.basecells_to_excel_ref(s.cells) == "A1:A25"
    assert filters.contains_string("A").explain == "Contains string: A"


def test_filter_does_not_contain_string(selectable_simple1: Selectable):
    """
    Test the not_contains_string filter behaves as expected
    """

    s = selectable_simple1.excel_ref("A1:B2").filter(filters.not_contains_string("A"))
    assert len(s.cells) == 2
    assert dfc.basecells_to_excel_ref(s.cells) == "B1:B2"
    assert filters.not_contains_string("A").explain == "Does not contain string: A"


def test_filter_is_numeric(selectable_vertical_dimensions: Selectable):
    """
    Test the is_numeric filter behaves as expected
    """

    s = (
        selectable_vertical_dimensions.excel_ref("D12:E19")
        .is_not_blank()
        .filter(filters.is_numeric)
    )
    assert len(s.cells) == 10
    assert dfc.basecells_to_excel_ref(s.cells) == "D14:E18"
    assert filters.is_numeric.explain == "Cell value is numeric"


def test_filter_is_not_numeric(selectable_vertical_dimensions: Selectable):
    """
    Test the is_not_numeric filter behaves as expected
    """

    s = (
        selectable_vertical_dimensions.excel_ref("D12:E19")
        .is_not_blank()
        .filter(filters.is_not_numeric)
    )
    assert len(s.cells) == 2
    assert dfc.basecells_to_excel_ref(s.cells) == "D12:E12"
    assert filters.is_not_numeric.explain == "Cell value is not numeric"
