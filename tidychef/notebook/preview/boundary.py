from typing import List

from tidychef import datafuncs as dfc
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import LiveTable


class Boundary:
    """
    Class to calculate and help manage the boundary of
    the cells we wish to display in this preview.
    """

    def __init__(
        self,
        selections: List[LiveTable],
        bounded: str = None,
        selection_boundary: bool = False,
    ):
        """
        Created a boundary to calculate the size of the
        preview that should be generated.

        :param selections: A list of all current selections
        :param bounded: An optional excel style reference to
        constrain the size of the previewed table.
        """

        assert not all([selection_boundary, bounded])
        if selection_boundary:
            assert len(selections) == 1
            selection = selections[0].cells
        else:
            selection = selections[0].pcells

        self.bounded = bounded
        if bounded is None:
            self.max_selected_x: int = dfc.maximum_x_offset(selection)
            self.max_selected_y: int = dfc.maximum_y_offset(selection)
            self.min_selected_x: int = dfc.minimum_x_offset(selection)
            self.min_selected_y: int = dfc.minimum_y_offset(selection)

        else:
            cells_wanted = dfc.multi_excel_ref_to_basecells(bounded)
            (
                self.min_selected_x,
                self.max_selected_x,
                self.min_selected_y,
                self.max_selected_y,
            ) = dfc.get_outlier_indicies(cells_wanted)

        # Where there's space, put a 1 cell blank border around walk
        # selections
        if selection_boundary:
            self.max_selected_x = (
                self.max_selected_x + 1
                if dfc.maximum_x_offset(selections[0].pcells) > self.max_selected_x
                else self.max_selected_x
            )
            self.min_selected_x = (
                self.min_selected_x - 1
                if dfc.minimum_x_offset(selections[0].pcells) < self.min_selected_x
                else self.min_selected_x
            )
            self.max_selected_y = (
                self.max_selected_y + 1
                if dfc.maximum_y_offset(selections[0].pcells) > self.max_selected_y
                else self.max_selected_y
            )
            self.min_selected_y = (
                self.min_selected_y - 1
                if dfc.minimum_y_offset(selections[0].pcells) < self.min_selected_y
                else self.min_selected_y
            )

    @property
    def highest_point(self):
        """
        The highest point of the table that we wish to preview, as you look at it
        """
        return self.min_selected_y

    @property
    def lowest_point(self):
        """
        The lowest point of the table that we wish to preview, as you look at it
        """
        return self.max_selected_y

    @property
    def leftmost_point(self):
        """
        The leftmost point of the table that we wish to preview, as you look at it
        """
        return self.min_selected_x

    @property
    def rightmost_point(self):
        """
        The rightmost point of the table that we wish to preview, as you look at it
        """
        return self.max_selected_x

    def contains(self, cell: Cell) -> bool:
        """
        Is the provided cell within the defined boundary of what we
        want to display as a preview.
        """
        return all(
            [
                cell.x >= self.min_selected_x,
                cell.x <= self.max_selected_x,
                cell.y >= self.min_selected_y,
                cell.y <= self.max_selected_y,
            ]
        )
