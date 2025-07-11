from dataclasses import dataclass
from typing import Dict, Optional

from tidychef.direction.directions import Direction
from tidychef.exceptions import AmbiguousLookupError, ImpossibleLookupError
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import LiveTable

from ..base import BaseLookupEngine

HIGHEST = 9999999999999
LOWEST = 0


@dataclass
class CellRange:
    """
    A class representing a range of cells

    :param low: the lowest index in the range
    :param high: the highest index in the range
    :param cell: the cell the spanning range resolves to
    :direction: the direction of traversal for the lookup
    """

    low: int
    high: int
    cell: Cell
    direction: Direction

    @property
    def axis_text(self) -> str:
        return "horizontal/x" if self.direction.is_horizontal else "vertical/y"

    def contains(self, cell: Cell) -> bool:
        """
        Does this cell contain the range
        in question.

        :param cell: The cell we want to check is in the range
        """
        if self.direction.is_horizontal:
            offset = cell.x
        else:
            offset = cell.y

        return offset >= self.low and offset <= self.high

    def spans_higher_range_than(self, cell: Cell) -> bool:
        """
        Does this range cover a range of indexes higher that the
        index of a given cell.

        :param cell: The cell this range may or may not span a higher
        range than.
        """
        if self.direction.is_horizontal:
            return self.low > cell.x
        else:
            return self.low > cell.y

    def spans_lower_range_than(self, cell: Cell) -> bool:
        """
        Does this range cover a range of indexes lower that the
        index of a given cell.

        :param cell: The cell this range may or may not span a lower
        range than.
        """
        if self.direction.is_horizontal:
            return self.high < cell.x
        else:
            return self.high < cell.y

    def _as_dict(self):
        return {
            "starts_at": str(self.low),
            "ends_at": str(self.high),
            "cell": str(self.cell),
            "axis": str(self.axis_text),
        }


class CellRanges:
    """
    A class representing multiple cell ranges
    """

    def __init__(self, selection: LiveTable, direction: Direction, table: str):
        """
        selection: The selection of cells to create the cell ranges from
        :direction: The direction of traversal considered when constructing ranges
        """
        self.direction: Direction = direction
        self.highest_possible_offset: Optional[int] = None
        self.lowest_possible_offset: Optional[int] = None
        self.table = table
        self._populate(selection)

    @property
    def axis_text(self) -> str:
        return "horizontal/x" if self.direction.is_horizontal else "vertical/y"

    def get_range_by_index(self, index: int) -> CellRange:
        """
        Get a single constructed range by index

        :param index: Index of the range to get
        """
        return self.ordered_cell_ranges[index]

    def _populate(self, selection: LiveTable):
        """
        Create the cell ranges from the selection provided

        :param selection: The selection of cells.
        """

        break_points = {}
        for cell in selection.cells:
            axis_offset = cell.x if self.direction.is_horizontal else cell.y
            if axis_offset in break_points.keys():
                raise AmbiguousLookupError(
                    f"""
                    Aborted while processing table "{self.table}.
                    
                    You have defined two or more equally valid closest:{self.direction.name}" relationships,
                    you cannot do this as it creates an ambiguous lookup.
                    
                    You are trying to add '{cell}' but we already have: '{break_points[axis_offset]}'.
                    
                    Both of these cells have a {self.axis_text} offsets of '{axis_offset}'. 
                    and so are equally close along this axis from any given observation cell.
                    """
                )
            break_points.update({axis_offset: cell})

        ordered_break_points = [int(k) for k in break_points.keys()]
        assert len(ordered_break_points) == len(selection.cells)
        ordered_break_points.sort()

        self.ordered_cell_ranges: Dict[int, CellRange] = {}

        if self.direction.is_left or self.direction.is_upwards:
            for i in range(0, len(ordered_break_points)):

                low = ordered_break_points[i]

                if i == 0:
                    self.lowest_possible_offset = low

                if i == len(ordered_break_points) - 1:
                    high = HIGHEST
                    self.highest_possible_offset = HIGHEST
                else:
                    high = ordered_break_points[i + 1] - 1

                self.ordered_cell_ranges[i] = CellRange(
                    low=low,
                    high=high,
                    cell=break_points[ordered_break_points[i]],
                    direction=self.direction,
                )

        else:
            for i in range(0, len(ordered_break_points)):

                high = ordered_break_points[i]

                if i == len(ordered_break_points) - 1:
                    self.highest_possible_offset = high

                if i == 0:
                    low = LOWEST
                    self.lowest_possible_offset = LOWEST
                else:
                    low = ordered_break_points[i - 1] + 1

                self.ordered_cell_ranges[i] = CellRange(
                    low=low,
                    high=high,
                    cell=break_points[ordered_break_points[i]],
                    direction=self.direction,
                )

        assert len(self.ordered_cell_ranges) == len(selection.cells)

    def _as_dict(self):
        """
        Reproduce the defined ranges as a dict.
        This functionality is purely for debugging and test purposes.
        """
        d = {}
        cell_range: CellRange
        for i, cell_range in self.ordered_cell_ranges.items():
            d.update({str(i): cell_range._as_dict()})
        return d


class Closest(BaseLookupEngine):
    def __init__(
        self,
        label: str,
        selection: LiveTable,
        direction: Direction,
        table: str = "Unnamed Table",
    ):
        """
        Creates a lookup engine to column values defined via
        the closest visual relationship.

        :param label: The label of the column informed
        by this lookup engine.
        :param: direction: one of up,down,left,right,above,below
        :param: Selection: the selection of cells that hold the column values being looked to.
        :param table: the name of the table data is being extracted from
        """
        self.table = table
        self.direction = direction
        self.ranges = CellRanges(selection, direction, table)
        self.bumped = True
        self.start_index = None
        self.label = label

    def _resolve_at_lower_range(self, index, cell, ceiling, floor):
        """
        Move the index down as as the cell offset was down/less-than the
        last ranged we looked at then attempt to resolve again.

        :param index: The index of the last range we looked at
        :param cell: The cell we're trying to find the correct range for
        :param ceiling: The highest range index to consider
        :param floor: The lowest range index to consider
        """

        if self.bumped is False and index != 0:
            new_index = index - 1
            self.bumped = True
        else:
            potential_range = ceiling - floor
            new_index = index - int(potential_range / 2)
            new_index = new_index if new_index != index else new_index - 1

        if new_index < 0:
            new_index = 0

        return self.resolve(cell, index=new_index, ceiling=index, floor=floor)

    def _resolve_at_higher_range(self, index, cell, ceiling, floor):
        """
        Move the index down as as the cell offset was above/greater-than the
        last ranged we looked at then attempt to resolve again.

        :param index: The index of the last range we looked at
        :param cell: The cell we're trying to find the correct range for
        :param ceiling: The lowest range index to consider
        :param floor: The highest range index to consider
        """

        if self.bumped is False and index != len(self.ranges.ordered_cell_ranges):
            new_index = index + 1
            self.bumped = True
        else:
            potential_range = ceiling - floor
            new_index = index + int(potential_range / 2)
            new_index = new_index if new_index != index else new_index + 1

        return self.resolve(cell, index=new_index, ceiling=ceiling, floor=index)

    def _confirm_within_bounds(self, cell: Cell):
        """
        Raise an exception if we're trying to resolve a lookup for a
        cell that is out of bounds, making a lookup impossible.

        example: we're trying to resolve a closest relations to the left
        of a cell that is further to the left than any of the ranges we're
        considering.

        :param cell: The single Cell object we want to resolve a the relative
        column cell object for.
        """

        err_str = """
                When processing table {table}. And column '{label}'.

                Lookup for observation cell '{cell}' is impossible. No
                cells in your selection exist in direction '{direction.name}'
                relative to this cell.

                The boundary (furthest cell index) out of the cells you provided
                on the `{axis}` axis has an offset of `{boundary}`.
                """

        out_of_bounds = [
            self.direction.is_upwards
            and cell.is_above(self.ranges.lowest_possible_offset),
            self.direction.is_downwards
            and cell.is_below(self.ranges.highest_possible_offset),
            self.direction.is_left
            and cell.is_left_of(self.ranges.lowest_possible_offset),
            self.direction.is_right
            and cell.is_right_of(self.ranges.highest_possible_offset),
        ]

        if True in out_of_bounds:
            axis = "x" if self.direction.is_horizontal else "y"
            raise ImpossibleLookupError(
                err_str.format(
                    table=self.table,
                    label=self.label,
                    cell=cell,
                    direction=self.direction,
                    axis=axis,
                    boundary=self.ranges.lowest_possible_offset
                    if any([self.direction.is_upwards, self.direction.is_left])
                    else self.ranges.highest_possible_offset,
                )
            )

    def resolve(self, cell: Cell, index=None, ceiling=None, floor=0) -> Cell:
        """
        Given the cell we want to lookup the relative column value for, use
        a bisection search to identify the correct range in our ordered list of ranges.

        Note - this method is called recursively, using the kwargs to start
        again at a different point in the indexed list of ranges.

        :param index: The index of the last range we looked at
        :param cell: The cell we're trying to find the correct range for
        :param ceiling: The lowest range index to consider
        :param floor: The highest range index to consider
        :return: The tidychef Cell object representing the
        column cell.
        """

        # If neither the index or ceiling have been passed in, then its the
        # very first lookup - confirm cell is within the bounds and therefore
        # this lookup is theoretically possible.
        if not ceiling and not index:
            self._confirm_within_bounds(cell)

        # If no maximum cell range (ceiling) is set then its the absolute maximum
        if ceiling is None:
            ceiling: int = len(self.ranges.ordered_cell_ranges) - 1

        if index is None:
            # When starting range index is not passed in, start at the mid point.
            mid_point: int = int(len(self.ranges.ordered_cell_ranges) / 2)
            index = list(self.ranges.ordered_cell_ranges.keys())[mid_point]

        considered_range: CellRange = self.ranges.get_range_by_index(index)

        if considered_range.spans_lower_range_than(cell):
            return self._resolve_at_higher_range(
                index, cell, ceiling=ceiling, floor=floor
            )
        elif considered_range.spans_higher_range_than(cell):
            return self._resolve_at_lower_range(
                index, cell, ceiling=ceiling, floor=floor
            )
        else:
            # Lookup Caching
            # --------------
            # cells are implicitly selected right->down-a-row->right as you look at a tabulated
            # (i.e as per standard human reading convention) so we'll cache this range index as
            # there's a significant chance the next obs lookup is in the same range
            #
            # this right-then-down-then-right pattern also means that (often, not guaranteed),
            # if the next obs isn't in the last range checked, there's a decent chance it's in a
            # neighbouring range, so we'll also always "bump" the index once in the relevant
            # direction on a first miss.
            self.index = index
            self.bumped = False

            return considered_range.cell
