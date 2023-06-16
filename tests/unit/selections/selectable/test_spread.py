import copy

import pytest

from datachef import acquire
from datachef.cardinal.directions import down, left, right, up
from datachef.selection.selectable import Selectable


def test_spread_standard_directions():
    """
    Confirm the the spread method works as expected with simple
    unextended cardinal directions.
    """

    s: Selectable = acquire.python.list_of_lists(
        [
            #  A      B        C        D      E
            ["   ", "   ", "       ", "   ", "   "],  # 1
            ["   ", "   ", "       ", "   ", "   "],  # 2
            ["   ", "foo", "bar    ", "baz", "   "],  # 3
            ["   ", "   ", "       ", "   ", "   "],  # 4
            ["   ", "   ", "blocked", "   ", "   "],  # 5
            ["   ", "   ", "       ", "   ", "   "],  # 6
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

    # if the cell labelled 'blocked' is included in the selection
    # it will also spread in the down direction
    d = s.is_not_blank()
    d = d.spread(down)
    assert len(d.cells) == 12
    assert d.excel_ref("C3").lone_value().strip() == "bar"
    assert d.excel_ref("C4").lone_value().strip() == "bar"
    assert d.excel_ref("C5").lone_value() == "blocked"
    assert d.excel_ref("C6").lone_value() == "blocked"

    # if call 'blocked' is not included in the selection
    # the spread of 'bar' will stop upon encountering that
    # non blank cell.
    d = s.excel_ref("B3:E3").is_not_blank()
    d = d.spread(down)
    assert len(d.cells) == 10

    # Check bad direction arguments raise a value error
    with pytest.raises(ValueError):
        s.spread("not-a-direction")


def test_spread_with_until():
    """
    Confirm we can pass in a selection as "until" that
    blocks the spread of cells.
    """

    s: Selectable = acquire.python.list_of_lists(
        [
            #  A      B        C        D      E
            ["   ", "   ", "       ", "   ", "   "],  # 1
            ["   ", "   ", "       ", "   ", "   "],  # 2
            ["   ", "foo", "bar    ", "baz", "   "],  # 3
            ["   ", "   ", "       ", "   ", "   "],  # 4
            ["   ", "   ", "       ", "   ", "   "],  # 5
            ["   ", "   ", "       ", "   ", "   "],  # 6
        ]
    )

    until = s.excel_ref("B5").expand(right)
    selected = s.excel_ref("B3").expand(right).is_not_blank().spread(down, until=until)
    assert len(selected.cells) == 6


def test_spread_exceptions():
    """
    Test that malformed or bad parameters to spread raise appropriate errors
    """

    s: Selectable = acquire.python.list_of_lists([])

    # Check bad direction arguments raise a value error
    with pytest.raises(ValueError):
        s.spread("not-a-direction")

    with pytest.raises(ValueError):
        bad_direction = copy.deepcopy(up)
        bad_direction.name = "whoops!"
        s.spread(bad_direction)
