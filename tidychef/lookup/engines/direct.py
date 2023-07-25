from typing import List

from tidychef import datafuncs as dfc
from tidychef.direction.directions import BaseDirection, Direction
from tidychef.exceptions import (
    FailedLookupError,
    MissingDirectLookupError,
    UnknownDirectionError,
)
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import LiveTable

from ..base import BaseLookupEngine


class Directly(BaseLookupEngine):
    """
    A class to resolve a direct lookup between
    a given observation cell and the appropriate
    cell from the selection of cells this class
    is constructed with.

    This appropriate cell is resolved based on the
    specified cardinal direction.

    Where no value exists in the direction specified
    an exception is raised.
    """

    def __init__(
        self,
        label: str,
        selection: LiveTable,
        direction: Direction,
        table: str = "Unnamed Table",
    ):
        """
        A class to resolve a direct lookup between
        a given observation cell and the appropriate
        cell from the selection of cells this class
        is constructed with.

        :param label: The label of the column informed
        by this lookup engine.
        :param: direction: one of up,down,left,right,above,below
        :param: Selection: the selection of cells that hold the column values being looked to.
        :param table: the name of the table data is being extracted from
        """
        self.table = table
        self.label = label
        self.direction: Direction = direction
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
        if self.direction.is_left or self.direction.is_upwards:
            ordered_cells = dfc.order_cells_leftright_topbottom(cells)
        elif self.direction.is_right or self.direction.is_downwards:
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

        :param cell: The tidychef Cell object we're trying
        to resolve the relative column cell object for.
        """
        if self.direction.is_horizontal:
            return cell.y
        return cell.x

    def resolve(self, cell: Cell) -> Cell:
        """
        Given an observation cell, return the
        appropriate cell as declared via this
        visual relationship.

        :param cell: The tidychef Cell object we're trying
        to resolve the relative column cell object for.
        :return: The tidychef Cell object representing the
        column cell.
        """

        potential_cells: List[Cell] = self._lookups.get(self._index(cell))
        if not potential_cells:
            raise MissingDirectLookupError(
                f"""
                When processing table "{self.table}" a direct lookup for column
                "{self.label}" failed because no column value exists in your
                column selection with direction: "{self.direction.name}" relative
                to the observation cell being resolved.
                
                The observation cell in question is:
                {cell._excel_ref()}, x position "{cell.x}", y position "{cell.y}",
                value: "{cell.value}"
            """
            )

        checker = {
            "left": lambda cell, pcell: cell.x > pcell.x,
            "right": lambda cell, pcell: cell.x < pcell.x,
            "up": lambda cell, pcell: cell.y > pcell.y,
            "above": lambda cell, pcell: cell.y > pcell.y,
            "down": lambda cell, pcell: cell.y < pcell.y,
            "below": lambda cell, pcell: cell.y < pcell.y,
        }

        chosen_cell = None
        for pcell in potential_cells:
            if checker[self.direction.name](cell, pcell):
                chosen_cell = pcell
            else:
                break

        if not chosen_cell:
            raise FailedLookupError(
                f"""
                When processing table "{self.table}" a Direct lookup for
                column "{self.label}" could not resolve with direction:
                "{self.direction.name}".

                The observation cell in question is:
                {cell._excel_ref()}, x position "{cell.x}", y position "{cell.y}",
                value: "{cell.value}"
                    """
            )

        return chosen_cell
