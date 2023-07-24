import copy
from dataclasses import dataclass

import pytest

from tidychef.direction.directions import Direction, above, below, down, left, right, up
from tidychef.selection.selectable import _reverse_direction


def test_reverse_direction():
    """
    Test that all directions are correctly reversed.
    """

    @dataclass
    class Case:
        original: Direction
        reversed: Direction

    for case in [
        Case(original=up, reversed=down),
        Case(original=down, reversed=up),
        Case(original=above, reversed=down),
        Case(original=below, reversed=up),
        Case(original=left, reversed=right),
        Case(original=right, reversed=left),
    ]:

        assert _reverse_direction(case.original) == case.reversed


def test_reverse_direction_exception():
    """
    An exception should be thrown if we pass an
    direction with an unknown name to reverse
    direction.
    """

    bad_up: Direction = copy.deepcopy(up)
    bad_up.name = "nope"

    with pytest.raises(Exception):
        _reverse_direction(bad_up)
