import pytest

from pivoter.selection.base import Selectable
from pivoter.utils.preview import HtmlPreview
from tests.fixtures.preconfigured import fixture_simple_one_tab


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


def test_preview(table_simple_as_xls1: Selectable):
    s = table_simple_as_xls1.excel_ref("F2:F10")
    s = s | table_simple_as_xls1.excel_ref("H6")
    p = HtmlPreview(s)
    p.print(path="here.html")
