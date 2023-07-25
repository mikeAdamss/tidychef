from typing import List

from tidychef import datafuncs as dfc
from tidychef.direction.directions import Direction
from tidychef.exceptions import ImpossibleLookupError, WithinAxisDeclarationError
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import LiveTable

from ..base import BaseLookupEngine


class Within(BaseLookupEngine):
    def __init__(
        self,
        label: str,
        selection: LiveTable,
        direction: Direction,
        start: Direction,
        end: Direction,
        table: str = "Unnamed Table",
    ):
        """
        Creates a lookup engine to resolve a Within lookup.

        Imagine the following example:

        |  A   |  B   |  C   |  D   |  E   |  F   |  G   |
        |------|------|------|------|------|------|------|
        |      |      |      |      |      |      |      |
        |      | age1 |      |      |      | age2 |      |
        | ob1  | ob2  | ob3  |      | ob4  | ob5  | ob6  |

        The relationships between the age dimension (age1 and age2 in the example)
        is both LEFT and RIGHT, relative to a given observation.

        Consider the following code:
        Within(cells, up, from=left(1), to=right(1))

        This is specifying age is above the observation, but only within the range of
        one to the left through 1 to the right.

        So in that example, we're searching (from the observation) for an age dimension
        cell via the following pattern.

        |   A  |  B   |  C   |  D   |
        |------|------|------|------|
        |   7  |  8   |  9   |      |
        |   4  |  5   |  6   |      |
        |   1  |  2   |  3   |      |
        |      |  ob  |      |      |

        With the header cell we're "looking up" being the first of the cells we've labelled
        1-9 (in that order) that is a cell we've also defined via the selection parameter.

        :param label: The label of the column informed
        by this lookup engine.
        :param Selection: the selection of cells that hold the column values being looked to.
        :param direction: cardinal direction declaration.
        :param start: a direction with an altered positional offset to indicate beginning of
        cell range to scan.
        :param end: a direction with an altered positional offset to indicate end of
        cell range to scan.
        :param table: the name of the table data is being extracted from
        """
        self.label = label
        self.table = table

        # Don't allow incorrect construction
        invalid_combinations = [
            start.is_horizontal and end.is_vertical,
            start.is_vertical and end.is_horizontal,
        ]

        if True in invalid_combinations:
            raise WithinAxisDeclarationError(
                f"""
                An error was encountered when processing column
                "{self.label}" of table "{self.table}" using a 
                within lookup.

                A Within class can only be constructed using two offset
                directions along a single axis.
                                             
                So you CAN combine
                - left, right
                - above, below
                - up, down
                etc
            
                You CANNOT combine
                - left, up
                - down, right
                etc
                                             
                As we're no longer scanning along a single axis.
                                             
                You provided:
                - name: "{start.name}", class: {start}
                - name: "{end.name}", class: {end} 
            """
            )

        self.start: Direction = start
        self.end: Direction = end
        self.direction_of_travel: Direction = end
        self.direction = direction

        self.cells: List[Cell] = selection.cells

    def _order(self, cells: List[Cell]) -> List[Cell]:
        """
        Order cells appropriately based on how the lookup engine has been configured

        :param cells: A list of cells to be ordered.
        :return: The ordered list of cells.
        """

        # Right
        if any([self.direction_of_travel.is_right and self.direction.is_downwards]):
            return dfc.order_cells_leftright_topbottom(cells)
        elif any([self.direction_of_travel.is_right and self.direction.is_upwards]):
            return dfc.order_cells_leftright_bottomtop(cells)

        # Left
        elif any([self.direction_of_travel.is_left and self.direction.is_downwards]):
            return dfc.order_cells_rightleft_topbottom(cells)
        elif any([self.direction_of_travel.is_left and self.direction.is_upwards]):
            return dfc.order_cells_rightleft_bottomtop(cells)

        # Downwards
        elif any([self.direction_of_travel.is_downwards and self.direction.is_right]):
            return dfc.order_cells_topbottom_leftright(cells)
        elif any([self.direction_of_travel.is_downwards and self.direction.is_left]):
            return dfc.order_cells_topbottom_rightleft(cells)

        # Upwards
        elif any([self.direction_of_travel.is_upwards and self.direction.is_right]):
            return dfc.order_cells_bottomtop_leftright(cells)
        elif any([self.direction_of_travel.is_upwards and self.direction.is_left]):
            return dfc.order_cells_bottomtop_rightleft(cells)

    def _feasible_cells(self, cell: Cell) -> List[Cell]:
        """
        Filters cells known to the engine to create a list of cells that are
        valid within the start= and end= params relative to the cell in question.

        :param cell: The tidychef cell we're trying to resolve the column
        cell for.
        :return: A list of cells that are feasible
        """

        if self.direction_of_travel.is_right and self.direction.is_upwards:
            x_start = cell.x + self.start.x
            x_end = cell.x + self.end.x
            return [
                c
                for c in self.cells
                if all([c.x >= x_start, c.x <= x_end, c.is_above(cell.y)])
            ]

        if self.direction_of_travel.is_left and self.direction.is_upwards:
            x_start = cell.x + self.end.x
            x_end = cell.x + self.start.x
            return [
                c
                for c in self.cells
                if all([c.x >= x_start, c.x <= x_end, c.is_above(cell.y)])
            ]

        if self.direction_of_travel.is_right and self.direction.is_downwards:
            x_start = cell.x + self.start.x
            x_end = cell.x + self.end.x
            return [
                c
                for c in self.cells
                if all([c.x >= x_start, c.x <= x_end, c.is_below(cell.y)])
            ]

        if self.direction_of_travel.is_left and self.direction.is_downwards:
            x_start = cell.x + self.end.x
            x_end = cell.x + self.start.x
            return [
                c
                for c in self.cells
                if all([c.x >= x_start, c.x <= x_end, c.is_below(cell.y)])
            ]

        if self.direction_of_travel.is_upwards and self.direction.is_right:
            y_start = cell.y + self.end.y
            y_end = cell.y + self.start.y
            return [
                c
                for c in self.cells
                if all([c.y >= y_start, c.y <= y_end, c.is_right_of(cell.x)])
            ]

        if self.direction_of_travel.is_upwards and self.direction.is_left:
            y_start = cell.y + self.end.y
            y_end = cell.y + self.start.y
            return [
                c
                for c in self.cells
                if all([c.y >= y_start, c.y <= y_end, c.is_left_of(cell.x)])
            ]

        if self.direction_of_travel.is_downwards and self.direction.is_left:
            y_start = cell.y + self.start.y
            y_end = cell.y + self.end.y
            return [
                c
                for c in self.cells
                if all([c.y >= y_start, c.y <= y_end, c.is_left_of(cell.x)])
            ]

        if self.direction_of_travel.is_downwards and self.direction.is_right:
            y_start = cell.y + self.start.y
            y_end = cell.y + self.end.y
            return [
                c
                for c in self.cells
                if all([c.y >= y_start, c.y <= y_end, c.is_right_of(cell.x)])
            ]

    def resolve(self, cell: Cell) -> Cell:
        """
        Given an observation cell, return the
        appropriate cell as declared via this
        visual relationship.

        :param cell: The tidychef Cell we want to resolve a column Cell for.
        :return: The column Cell we're resolved.
        """

        assert isinstance(cell, Cell)

        # Discard non feasible cells to avoid the overhead of ordering
        # cells that cant be the lookup
        feasible_cells = self._feasible_cells(cell)

        if len(feasible_cells) == 0:
            raise ImpossibleLookupError(
                f"""
                An error was encountered when processing column
                "{self.label}" of table "{self.table}" using a 
                within lookup.

                Within lookup cannot be resolved, there is no
                cell to find within the constraints:
                                        
                Start:  {self.start}
                End:    {self.end}

                Direction of traversal:
                {self.direction}

                Relative to observation cell {cell}

                Column cells were:
                {self.cells}                    
                """
            )
        ordered_feasible_cells = self._order(feasible_cells)
        assert len(ordered_feasible_cells) == len(feasible_cells)

        if self.direction.is_left:
            max_x = max([x.x for x in ordered_feasible_cells])
            for cell in ordered_feasible_cells:
                if cell.x == max_x:
                    return cell

        if self.direction.is_upwards:
            max_y = max([x.y for x in ordered_feasible_cells])
            for cell in ordered_feasible_cells:
                if cell.y == max_y:
                    return cell

        if self.direction.is_right:
            min_x = min([x.x for x in ordered_feasible_cells])
            for cell in ordered_feasible_cells:
                if cell.x == min_x:
                    return cell

        if self.direction.is_downwards:
            min_y = min([x.y for x in ordered_feasible_cells])
            for cell in ordered_feasible_cells:
                if cell.y == min_y:
                    return cell
