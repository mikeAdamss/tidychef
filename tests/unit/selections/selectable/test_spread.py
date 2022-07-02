import pytest

from datachef import acquire
from datachef.cardinal.directions import down, left, right, up
from datachef.selection.selectable import Selectable


def test_spread_standard_directions():
    """
    Confirm the the spread method works as expected with simple
    unextended cardinal directions.
    """

    s: Selectable = acquire(
        [
            ["   ", "   ", "       ", "   ", "   "],
            ["   ", "   ", "       ", "   ", "   "],
            ["   ", "foo", "bar    ", "baz", "   "],
            ["   ", "   ", "       ", "   ", "   "],
            ["   ", "   ", "blocked", "   ", "   "],
            ["   ", "   ", "       ", "   ", "   "],
        ]
    )

    r = s.is_not_blank()
    r = r.spread(right)
    assert len(r.cells) == 7
    assert r.excel_ref("E3").lone_value() == "baz"

    l = s.is_not_blank()
    l = l.spread(left)
    assert len(l.cells) == 7
    assert l.excel_ref("A3").lone_value() == "foo"

    u = s.is_not_blank()
    u = u.spread(up)
    assert len(u.cells) == 11
    assert u.excel_ref("B1").lone_value() == "foo"
    assert u.excel_ref("B2").lone_value() == "foo"

    # if call 'blocked' is included in the selection
    # that vall value will be spread.
    d = s.is_not_blank()
    d = d.spread(down)
    assert len(d.cells) == 12
    assert d.excel_ref("C3").lone_value().strip() == "bar"
    assert d.excel_ref("C4").lone_value().strip() == "bar"
    assert d.excel_ref("C5").lone_value() == "blocked"

    # if call 'blocked' is not included in the selection
    # the spread of 'bar' will stop upon encountering that
    # non blank cell.
    d = s.excel_ref("B3:E3").is_not_blank()
    d = d.spread(down)
    assert len(d.cells) == 10

    with pytest.raises(ValueError):
        s.spread("not-a-direction")
