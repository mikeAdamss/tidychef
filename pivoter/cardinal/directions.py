from typing import Optional
from dataclasses import dataclass


@dataclass
class BaseDirection:
    x: int
    y: int
    locked: bool = False
    horizontal_axis: Optional[bool] = None

    def __call__(self, relative_change: int):
        """
        Enables user friendly shifts along
        axis without dipping into raw xy positioning
        e,g: RIGHT(3), DOWN(5)
        """

        # Don't allow continual reinstantiaition of a direction
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
