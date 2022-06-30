import pytest

from datachef.selection import datafuncs as dfc
from datachef.selection.filters import contains_string
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_filter_contains_string(selectable_simple1: Selectable):
    """
    Test the contains string filter behaves as expected
    """

    s = selectable_simple1.excel_ref("A1:G25").filter(contains_string("A"))
    assert len(s.cells) == 25
    assert dfc.basecells_to_excel_ref(s.cells) == "A1:A25"
