import pytest

from tidychef.direction.directions import above, below, down, left, right, up
from tidychef.exceptions import CardinalDeclarationWithOffset


def test_cardinal_offset_can_be_overwritten():
    """
    Test that each cardinal direction denototes a single
    positional index in the direction in question and that
    we can extend the index where needed.
    """

    for direction, x_expected, y_expected in [
        [right, 1, 0],
        [right(1), 1, 0],
        [right(7), 7, 0],
        [right(53465), 53465, 0],
        [left, -1, 0],
        [left(1), -1, 0],
        [left(7), -7, 0],
        [left(53465), -53465, 0],
        [down, 0, 1],
        [down(1), 0, 1],
        [down(7), 0, 7],
        [down(53465), 0, 53465],
        [below, 0, 1],
        [below(1), 0, 1],
        [below(7), 0, 7],
        [below(53465), 0, 53465],
        [above, 0, -1],
        [above(1), 0, -1],
        [above(7), 0, -7],
        [above(53465), 0, -53465],
        [up, 0, -1],
        [up(1), 0, -1],
        [up(7), 0, -7],
        [up(53465), 0, -53465],
    ]:
        assert direction.x == x_expected
        assert direction.y == y_expected


def test_cardinal_offset_cannot_be_overwritten_twice():
    """
    Test that a user is blocked from overwriting a
    cardial directions offset more than once.
    """

    with pytest.raises(Exception):
        right(2)(2)


def test_confirm_pristine():
    """
    Test that we raise for non pristine directions
    where appropriate
    """

    # Should not raise
    up._confirm_pristine()

    # Should raise
    with pytest.raises(CardinalDeclarationWithOffset):
        up(2)._confirm_pristine()


def test_offset_as_str():
    """
    Confirm that we can get a plain english summary
    of the specified direction and the degree of its
    principle offset
    """

    assert up(2).offset_as_str == "up(2)"
    assert left(18).offset_as_str == "left(18)"
    assert down.offset_as_str == "down(1)"
    assert right(4).offset_as_str == "right(4)"
