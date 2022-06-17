from typing import List

from pivoter.exceptions import LoneValueOnMultipleCellsError
from pivoter.models.source.cell import BaseCell
from pivoter.models.source.input import BaseInput
from pivoter.constants import UP, DOWN, LEFT, RIGHT

class Selectable(BaseInput):
    """
    Selection methods that are (now and in the future)
    generic to all tabulated source inputs.
    """

    def lone_value(self) -> str:
        """
        Confirms the selection contains exactly one cell, then returns
        the value of that cell
        """
        if len(self.selected_table.filtered.cells) != 1:
            raise LoneValueOnMultipleCellsError(
                len(self.selected_table.filtered.cells)
            )
        return self.selected_table.filtered.cells[0].value


    def expand(self, DIRECTION):
        """
        Given a direction of UP, DOWN, LEFT, RIGHT, ABOVE or BELOW
        Expands the current selection of cells in that direction.
        """
        availible_cells = self.datamethods._unmatching_xy_cells_from_filtered(
            self, self.selected_table.pristine
        )

        all_y_indicies = set(
            c.y for c in self.selected_table.filtered
        )

        selection: List[BaseCell] = []

        if DIRECTION == UP or DIRECTION == DOWN:
            all_x_indicies = set(
                c.x for c in self.selected_table.filtered
            )
            for xi in all_x_indicies:
                cells_on_xi = self.datamethods._cells_on_x_index(self, xi)
                for cell in cells_on_xi:
                    cells_on_yi = self.datamethods._cells_on_y_index(self, cell.y)

                    if DIRECTION == UP:
                        selection += [
                            c1
                            for c1 in availible_cells
                            if any([c2 for c2 in cells_on_yi if c2.y < c1.y])
                        ]

                    if DIRECTION == DOWN:
                        selection += [
                            c1
                            for c1 in availible_cells
                            if any([c2 for c2 in cells_on_yi if c2.y > c1.y])
                        ]
      

        self.selected_table.filtered = self.datamethods._exactly_matched_xy_cells_from_filtered(self, selection)
        return self