import pytest

from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


def test_matching_xy_cells(fixture_simple_one_tab: XlsInputSelectable):
    ...
