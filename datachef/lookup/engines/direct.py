from typing import List

from datachef.cardinal.directions import Direction
from datachef.models.source.cell import Cell

from ..base import BaseLookup


class DirectEngine(BaseLookup):
    """
    A class representing a direct lookup.

    i.e for any given observation the required
    value is directly inline along either the
    vertical or horizontal axis.
    """

    def _post_init(self, cells: List[Cell], direction: Direction):
        """

        :param: The value items that define this
        component, eg: in case of a dimesion, these
        would be the dimensional values.
        """

        # Given we know the relationship is always
        # along a single axis, we'll create a
        # tiered dict so we can just pluck out
        # the required lookup cell using the
        # relevent x or y offset of the
        # observation cell in question.
        ...

    def lookup(self, cell: Cell) -> Cell:
        """
        Given an observation cell, return the
        appropriate cell as declared via this
        visual relationship.
        """
