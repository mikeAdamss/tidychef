from typing import List
from datachef.models.source.cell import BaseCell, Cell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable
from datachef.utils import cellutils

class Boundary:
    """
    Class to calculate and help manage the boundary of
    the cells we wish to display in this preview
    """

    def __init__(self, selections: List[Selectable], start:str = None, end: str = None, with_excel: bool = True):

        self.with_excel:bool = with_excel
        self.max_selected_x: int = max(dfc.maximum_x_offset(s.pcells) for s in selections)
        self.max_selected_y: int = max(dfc.maximum_y_offset(s.pcells) for s in selections)
        self.min_selected_x: int = min(dfc.minimum_x_offset(s.pcells) for s in selections)
        self.min_selected_y: int = min(dfc.minimum_y_offset(s.pcells) for s in selections)
        
        # If not cells have highlighted on all selection
        # i.e we're previewing the source as-is,
        # then it is considered pristine 
        self.is_pristine: bool = not all([s.selections_made() for s in selections])

        if start:
            if start != "selection":
                boundary_cell: BaseCell = dfc.single_excel_ref_to_basecell(start)
                assert (
                    boundary_cell.x > self.min_selected_x
                ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a column limit of {cellutils.x_to_letters(boundary_cell.x)} but have an x axis selection in column {cellutils.x_to_letters(self.min_selected_x)}"
                assert (
                    boundary_cell.y > self.min_selected_y
                ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a row limit of {cellutils.y_to_number(boundary_cell.y)} but have an y axis selection on row {cellutils.y_to_number(self.min_selected_y)}"
                self.min_selected_x = boundary_cell.x
                self.min_selected_y = boundary_cell.y
            elif start == 'selection':
                self.min_selected_x: int = min(dfc.minimum_x_offset(s.cells) for s in selections)
                self.min_selected_y: int = min(dfc.minimum_y_offset(s.cells) for s in selections)
        
        if end:
            if end != 'selection':
                boundary_cell: BaseCell = dfc.single_excel_ref_to_basecell(end)
                assert (boundary_cell.x < self.max_selected_x
                        ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a column limit of {cellutils.x_to_letters(boundary_cell.x)} but have an x axis selection in column {cellutils.x_to_letters(self.max_selected_x)}"
                assert (boundary_cell.y < self.max_selected_y
                    ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a row limit of {cellutils.y_to_number(boundary_cell.y)} but have an y axis selection on row {cellutils.y_to_number(self.max_selected_y)}"
                self.max_selected_x = boundary_cell.x
                self.max_selected_y = boundary_cell.y
            else:
                self.max_selected_x: int = max(dfc.maximum_x_offset(s.cells) for s in selections)
                self.max_selected_y: int = max(dfc.maximum_y_offset(s.cells) for s in selections)


    # Some syntactic sugar to make x and y positions easier to work with

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
                cell.y <= self.max_selected_y
            ]
        )

    def __repr__(self):
        """
        Simple print representing the defined boundary in a human readable way
        """
        left = cellutils.x_to_letters(self.leftmost_point) if self.with_excel else self.leftmost_point
        right = cellutils.x_to_letters(self.rightmost_point) if self.with_excel else self.rightmost_point
        top = cellutils.y_to_number(self.highest_point) if self.with_excel else self.leftmost_point
        bottom = cellutils.y_to_number(self.lowest_point) if self.with_excel else self.rightmost_point
            
        return (f'''
                {top}
                |
{left:>10} ---------- {right}
                |
                {bottom}
        ''')