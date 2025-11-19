import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.csv.csv import CsvSelectable


@pytest.fixture
def csv_selectable_simple1():
    """
    Create a CsvSelectable instance for testing formatting methods
    """
    # fixture_simple_one_tab() already returns a CsvSelectable instance
    return fixture_simple_one_tab()


def test_is_bold_raises_not_implemented_error(csv_selectable_simple1: CsvSelectable):
    """
    Test that is_bold() raises NotImplementedError for CsvSelectable class.
    """
    with pytest.raises(NotImplementedError) as exc_info:
        csv_selectable_simple1.is_bold()
    
    assert "Selectable CsvSelectable does not implement an is_bold() method" in str(exc_info.value)


def test_is_not_bold_raises_not_implemented_error(csv_selectable_simple1: CsvSelectable):
    """
    Test that is_not_bold() raises NotImplementedError for CsvSelectable class.
    """
    with pytest.raises(NotImplementedError) as exc_info:
        csv_selectable_simple1.is_not_bold()
    
    assert "Selectable CsvSelectable does not implement an is_not_bold() method" in str(exc_info.value)
