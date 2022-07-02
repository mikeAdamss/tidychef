import pytest

from datachef.cardinal.directions import down, left, right, up
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab
from datachef.readers.objects.list import ListReader
from datachef import acquire

@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_spread_standard_directions():
    """
    Confirm the the spread method works as expected with simple
    unextended cardinal directions.
    """

    s: Selectable = acquire(
        [
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', 'foo', 'bar', 'baz', ''],
            ['', '', '', '', '']
        ])

    r = s.is_not_blank().spread(right)
    assert len(r.cells) == 4
    assert r.excel_ref('E3').lone_value() == 'baz'

    l = s.is_not_blank().spread(left)
    assert len(l.cells) == 4
    assert l.excel_ref('A3').lone_value() == 'foo'

    u = s.is_not_blank().spread(up)
    assert len(u.cells) == 9
    assert u.excel_ref('B1').lone_value() == 'foo'
    assert u.excel_ref('B2').lone_value() == 'foo'

    d = s.is_not_blank().spread(down)
    assert len(d.cells) == 6
    assert d.excel_ref('C4').lone_value() == 'bar'
