from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseDirection:
    """
    A class representing a cardinal direction.

    :param x: The horizontal offset. For example:
    1 = one space, right, -1 = one position left.
    :param y: The vertical offset. For example:
    1 = one space down, -1 = one position left.
    """
    x: int
    y: int
    locked: bool = False
    horizontal_axis: Optional[bool] = None

    def __call__(self, relative_change: int):
        """
        Passing in an integer a parameter enables us to
        declare shifts along the xy axis (where applicable)
        without dipping into raw xy positioning
        e,g: RIGHT(3), DOWN(5).

        For example:
        
        RIGHT (the default) == (x:1, y:0) 
        So equates to a representation of one positive
        positional movement on the x axis.
        So RIGHT(3) == (x:4, y:0)

        LEFT == (x:-1, y:0)
        so LEFT(3) == (x:-4: y:0)

        :param relative_change: the amount to extend the
        positional integer by.
        """

        # Don't allow continual reinstantiaition of a direction
        # i.e RIGHT(3)(4) would be a mess.
        if self.locked:
            raise Exception(
                "You cannot modify a cardinal directions offset value more than once"
            )

        if self.horizontal_axis:
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
        return BaseDirection(x, y, locked=True)


UP = BaseDirection(0, -1, horizontal_axis=False)
DOWN = BaseDirection(0, 1, horizontal_axis=False)
RIGHT = BaseDirection(1, 0, horizontal_axis=True)
LEFT = BaseDirection(-1, 0, horizontal_axis=True)

# Aliases
ABOVE = UP
BELOW = DOWN
