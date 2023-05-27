from typing import List

from datachef.cardinal.directions import BaseDirection, Direction
from datachef.exceptions import (
    FailedLookupError,
    MissingDirectLookupError,
    UnknownDirectionError,
)
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable

from ..base import BaseLookupEngine


class Directly(BaseLookupEngine):
    """
    A class to resolve a direct lookup between
    an observation cell and the value from the
    """

    def __init__(self, selection: Selectable, direction: BaseDirection):
        """

        :param: The value items that define this
        component, eg: in case of a dimension, these
        would be the dimensional values.
        """
        self.direction: BaseDirection = direction
        cells = selection.cells

        # Given we know the relationship is always
        # along a single axis, we'll create a
        # dict so we can just pluck out
        # the required lookup cell using the
        # relevant x or y offset of the
        # observation cell in question.

        # The complication comes from having
        # multiple potential selections along
        # a single axis.

        # example:
        # ob = observation
        # dim.* = dimension item we're looking up
        #
        # | dim1.1 |     | ob  | ob  |     | dim2.1 |     | [ob]  |  [ob] |
        # | dim1.2 |     | ob  | ob  |     | dim2.2 |     | [ob]  |  [ob] |
        # | dim1.3 |     | ob  | ob  |     | dim2.3 |     | [ob]  |  [ob] |
        # | dim1.4 |     | ob  | ob  |     | dim2.4 |     | [ob]  |  [ob] |
        # | dim1.5 |     | ob  | ob  |     | dim2.5 |     | [ob]  |  [ob] |
        #
        # If you consider each [ob] cells and a lookup for direction:left,
        # there are two available dimensions on that axis, we need to
        # differentiate the correct one per ob.

        if not isinstance(self.direction, BaseDirection):
            raise UnknownDirectionError(
                f"The direction parameter must be of type: {type(BaseDirection)}"
            )
        if self.direction.name in ["left", "up"]:
            ordered_cells = dfc.order_cells_leftright_topbottom(cells)
        elif self.direction.name in ["right", "down"]:
            ordered_cells = dfc.order_cells_rightleft_bottomtop(cells)
        else:
            # Shouldn't happen
            raise UnknownDirectionError(f"The direction {direction.name} is unknown.")

        self._lookups = {}
        for cell in ordered_cells:
            if self._index(cell) not in self._lookups:
                self._lookups[self._index(cell)] = []
            self._lookups[self._index(cell)].append(cell)

    def _index(self, cell: Cell):
        """
        Get the x or y offset we're interested in.

        By default its the along the principle direction
        of travel, i.e cell.x (column index) for a
        horizontal lookups else y (row index).
        """
        if self.direction._horizontal_axis:
            return cell.y
        return cell.x

    def resolve(self, cell: Cell) -> Cell:
        """
        Given an observation cell, return the
        appropriate cell as declared via this
        visual relationship.
        """

        potential_cells: List[Cell] = self._lookups.get(self._index(cell))
        if not potential_cells:
            raise MissingDirectLookupError(
                f"We're using a direct lookup for but no selected cells have "
                f' been provided in the direction: "{self.direction.name}" '
                f"relative to cell: {cell._excel_ref()}, in x position {cell.x}, "
                f"y position {cell.y}"
            )

        checker = {
            "left": lambda cell, pcell: cell.x > pcell.x,
            "right": lambda cell, pcell: cell.x < pcell.x,
            "up": lambda cell, pcell: cell.y > pcell.y,
            "down": lambda cell, pcell: cell.y < pcell.y,
        }

        chosen_cell = None
        for pcell in potential_cells:
            if checker[self.direction.name](cell, pcell):
                chosen_cell = pcell
            else:
                break

        if not chosen_cell:
            raise FailedLookupError(
                f"Couldn't find a relative value for cell {cell}"
                f" with direction {self.direction.name}"
            )

        return chosen_cell
