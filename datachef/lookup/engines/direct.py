from typing import List

from datachef.cardinal.directions import Direction
from datachef.exceptions import (
    FailedLookupError,
    MissingDirectLookupError,
    UnknownDirectionError,
)
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable

from ..base import BaseLookup


class Direct(BaseLookup):
    """
    A class representing a direct lookup.

    i.e for any given observation the required
    value is directly inline along either the
    vertical or horizontal axis.
    """

    def _index(self, cell: Cell):
        """
        Get the x or y offset we're interested in.

        By default its the along the principle direction
        of travel, i.e cell.x (column index) for a
        horixontal lookups else y (row index).
        """
        if self.direction._horizontal_axis:
            return cell.y
        return cell.x

    def _post_init(self, selection: Selectable, direction: Direction):
        """

        :param: The value items that define this
        component, eg: in case of a dimesion, these
        would be the dimensional values.
        """
        self.direction: Direction = direction
        cells = selection.cells

        # Given we know the relationship is always
        # along a single axis, we'll create a
        # dict so we can just pluck out
        # the required lookup cell using the
        # relevent x or y offset of the
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
        # there are two availible dimesions on that axis, we need to
        # differentiate the correct one per ob.

        if self.direction._direction in ["left", "up"]:
            ordered_cells = dfc.order_cells_leftright_topbottom(cells)
        elif self.direction._direction in ["right", "down"]:
            ordered_cells = dfc.order_cells_rightleft_bottomtop(cells)
        else:
            raise UnknownDirectionError(
                f"The direction {direction._direction} is unknown."
            )

        self._lookups = {}
        for cell in ordered_cells:
            if self._index(cell) not in self._lookups:
                self._lookups[self._index(cell)] = []
            self._lookups[self._index(cell)].append(cell)

    def resolve(self, cell: Cell) -> Cell:
        """
        Given an observation cell, return the
        appropriate cell as declared via this
        visual relationship.
        """

        potential_cells: List[Cell] = self._lookups.get(self._index(cell))
        if not potential_cells:
            raise MissingDirectLookupError(
                f"We're using a direct lookup for {self.name} but there "
                f'are no specified value in the direction: "{self.direction._direction}" '
                f"relative to cell: {cell}, in x position {cell.x}, y position {cell.y}",
                f"Availible values are {self._lookups}",
            )

        checker = {
            "left": lambda cell, pcell: cell.x > pcell.x,
            "right": lambda cell, pcell: cell.x < pcell.x,
            "up": lambda cell, pcell: cell.y > pcell.y,
            "down": lambda cell, pcell: cell.y < pcell.y,
        }

        chosen_cell = None
        for pcell in potential_cells:
            if checker[self.direction._direction](cell, pcell):
                chosen_cell = pcell
            else:
                break

        if not chosen_cell:
            raise FailedLookupError(
                f"Couldn't find a relative value for cell {cell}"
                f"in {self.name} with direction {self.direction._direction}"
            )

        return chosen_cell
