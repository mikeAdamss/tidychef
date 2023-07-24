import pytest

from tidychef.direction import down, left, right, up
from tidychef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_explain(selectable_simple1: Selectable):
    """
    Write some explain statements to path
    to confirm expected behaviour
    """
    a = selectable_simple1.config(explain_path="explain.html")
    b = a.excel_ref("B")
    c = b.extrude(right(2))
    d = c.shift(left(1))
    e = d.excel_ref("A4:C20")
    f = e.re("^C.*$")
