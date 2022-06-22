import pytest

from pivoter.cardinal.directions import ABOVE, BELOW, DOWN, LEFT, RIGHT, UP


def test_cardinal_offset_can_be_overwritten():
    """
    Test that each cardinal direction denototes a single
    positional index in the direction in question and that
    we can extend the index where needed.
    """

    for direction, x_expected, y_expected in [
        [RIGHT, 1, 0],
        [RIGHT(1), 1, 0],
        [RIGHT(7), 7, 0],
        [RIGHT(53465), 53465, 0],
        [LEFT, -1, 0],
        [LEFT(1), -1, 0],
        [LEFT(7), -7, 0],
        [LEFT(53465), -53465, 0],
        [DOWN, 0, 1],
        [DOWN(1), 0, 1],
        [DOWN(7), 0, 7],
        [DOWN(53465), 0, 53465],
        [BELOW, 0, 1],
        [BELOW(1), 0, 1],
        [BELOW(7), 0, 7],
        [BELOW(53465), 0, 53465],
        [ABOVE, 0, -1],
        [ABOVE(1), 0, -1],
        [ABOVE(7), 0, -7],
        [ABOVE(53465), 0, -53465],
        [UP, 0, -1],
        [UP(1), 0, -1],
        [UP(7), 0, -7],
        [UP(53465), 0, -53465],
    ]:
        assert direction.x == x_expected
        assert direction.y == y_expected


def test_cardinal_offset_cannot_be_overwritten_twice():
    """
    Test that a user is blocked from overwriting a
    cardial directions offset more than once.
    """

    with pytest.raises(Exception):
        RIGHT(2)(2)
