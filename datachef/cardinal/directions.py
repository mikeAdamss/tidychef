from dataclasses import dataclass
from typing import Optional

from datachef.exceptions import CardinalDeclarationWithOffset
from datachef.utils.decorators import dontmutate


class BaseDirection:
    ...


@dontmutate
@dataclass
class Direction(BaseDirection):
    """
    A class representing a cardinal direction.

    :param x: The horizontal offset. For example:
    1 = one space, right, -1 = one position left.
    :param y: The vertical offset. For example:
    1 = one space down, -1 = one position left.
    """

    x: int
    y: int
    name: str
    _locked: bool = False

    # TODO
    # police passing it over offset overides
    # where they should not be used

    @property
    def is_upwards(self) -> bool:
        """
        Is direction.name one of ["up", "above"]
        """
        return self.name in ["up", "above"]

    @property
    def is_downwards(self) -> bool:
        """
        Is direction.name one of ["down", "below"]
        """
        return self.name in ["down", "below"]

    @property
    def is_left(self) -> bool:
        """
        Is direction.name "left"
        """
        return self.name == "left"

    @property
    def is_right(self) -> bool:
        """
        Is direction.name "right"
        """
        return self.name == "right"

    @property
    def is_horizontal(self) -> bool:
        """
        Is left or right
        """
        return self.is_right or self.is_left

    def _confirm_pristine(self):
        """
        There are some cenarios where we want to disallow
        the passing in of directional offsets.
        """
        if self._locked:
            raise CardinalDeclarationWithOffset(
                """
                You cannot pass an offset into a direction
                in the context of declaring an absolute direction.
            
                i.e .expand(up) or .fill(up) is ok, expand(up(1)) or
                fill(up(1) is not.
                """
            )

    def __call__(self, relative_change: int):
        """
        Passing in an integer a parameter enables us to
        declare shifts along the xy axis (where applicable)
        without dipping into raw xy positioning
        e,g: right(3), down(5).

        For example:

        right (default) == (x:1, y:0)
        So equates to a representation of one positive
        positional movement on the x axis.
        So right(3) == (x:4, y:0)

        left == (x:-1, y:0)
        so left(3) == (x:-4: y:0)

        :param relative_change: the amount to extend the
        positional integer by.
        """

        # Don't allow continual overwriting of a directional offset
        # i.e right(3)(4) would be a mess.
        if self._locked:
            raise Exception(
                "You cannot modify a cardinal directions offset value more than once"
            )

        if self.is_horizontal:
            if self.x == -1:
                x = -relative_change
                y = self.y
            elif self.x == 1:
                x = relative_change
                y = self.y
        else:
            if self.y == -1:
                y = -relative_change
                x = self.x
            elif self.y == 1:
                y = relative_change
                x = self.x
        return Direction(x, y, self.name, _locked=True)


up = Direction(0, -1, "up")
above = Direction(0, -1, "above")
down = Direction(0, 1, "down")
below = Direction(0, 1, "below")
right = Direction(1, 0, "right")
left = Direction(-1, 0, "left")
