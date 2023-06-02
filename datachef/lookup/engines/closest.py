from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from datachef.cardinal.directions import Direction
from datachef.exceptions import AmbiguousLookupError, OutOfBoundsError
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable

from ..base import BaseLookupEngine

HIGHEST = 9999999999999
LOWEST = 0


@dataclass
class CellRange:
    """
    A class representing a range of cells
    """

    low: int
    high: int
    cell: Cell
    is_horizontal: bool

    @property
    def is_vertical(self) -> bool:
        return not self.is_horizontal

    def contains(self, cell: Cell) -> bool:
        """
        Does this cell contain the range
        in question.
        """
        if self.is_horizontal:
            offset = cell.x
        else:
            offset = cell.y

        return offset >= self.low and offset < self.high

    def spans_higher_range_than(self, cell: Cell) -> bool:
        """
        Does this range cover a range of indexes higher that the
        index of a given cell.
        """
        if self.is_horizontal:
            return self.low > cell.x
        else:
            return self.low > cell.y

    def spans_lower_range_than(self, cell: Cell) -> bool:
        """
        Does this range cover a range of indexes lower that the
        index of a given cell.
        """
        if self.is_horizontal:
            return self.high <= cell.x
        else:
            return self.high <= cell.y


class CellRanges:
    """
    A class representing multiple cell ranges
    """

    def __init__(self, cells: Selectable, direction: Direction):
        self.direction: Direction = direction
        self._populate(cells)

    @property
    def axis_text(self) -> str:
        return "horizontal/x" if self.is_horizontal else "vertical/y"

    @property
    def is_horizontal(self) -> bool:
        return self.direction._horizontal_axis

    def _populate(self, selection: Selectable):
        """ """

        break_points = {}
        for cell in selection.cells:
            axis_offset = cell.x if self.is_horizontal else cell.y
            if axis_offset in break_points.keys():
                raise AmbiguousLookupError(
                    f"""
                    Aborting. You have defined two or more equally valid closest:{self.direction.name}" relationships,
                    you cannot do this as it creates an ambiguous lookup.
                    
                    You are trying to add '{cell}' but we already have: '{break_points[axis_offset]}'.
                    
                    Both of these cells have a {self.axis_text} offsets of '{axis_offset}'. 
                    and so are equally close along this axis from a given observation cell.
                    """
                )
            break_points.update({axis_offset: cell})

        ordered_break_points = [int(k) for k in break_points.keys()]
        assert len(ordered_break_points) == len(selection.cells)
        ordered_break_points.sort()

        self.ordered_cell_ranges = {}

        print(ordered_break_points)
        if self.direction.is_left or self.direction.is_upwards:
            for i in range(0, len(ordered_break_points)):

                low = ordered_break_points[i]

                if i == len(ordered_break_points) - 1:
                    high = HIGHEST
                else:
                    high = ordered_break_points[i + 1]

                self.ordered_cell_ranges[i] = CellRange(
                    low=low,
                    high=high,
                    cell=break_points[ordered_break_points[i]],
                    is_horizontal=self.is_horizontal,
                )

        else:
            for i in range(0, len(ordered_break_points)):

                high = ordered_break_points[i]

                if i == 0:
                    low = LOWEST
                else:
                    low = ordered_break_points[i-1]

                self.ordered_cell_ranges[i] = CellRange(
                    low=low,
                    high=high,
                    cell=break_points[ordered_break_points[i]],
                    is_horizontal=self.is_horizontal,
                )

    def _as_dict(self):
        """
        Reproduce the defined ranges as a dict.
        This functionality is purely for debugging and test purposes.
        """
        d = {}
        cell_range: CellRange
        for i, cell_range in self.ordered_cell_ranges.items():
            d.update(
                {
                    str(i): {
                        "starts_at": str(cell_range.low),
                        "ends_at": str(cell_range.high),
                        "cell": str(cell_range.cell),
                        "axis": str(self.axis_text),
                    }
                }
            )
        return d


class Closest(BaseLookupEngine):
    def __init__(self, selection: Selectable, direction: Direction):
        """
        Creates a lookup engine for dimensions defined with the CLOSEST relationship.
        """
        self.direction = direction
        self.ranges = CellRanges(selection, direction)

    def _bump_as_too_low(self, index, cell, ceiling, floor):
        "move the index down as as the cell was beneath/less-than the last ranged we looked at"
        assert (
            index == ceiling
        ), "If we`re specified the cell is in a lower range, ceiling should be set to last index"
        if self.bumped == False and index != 0:
            index = index - 1
            self.bumped = True
        else:
            potential_range = ceiling - floor
            new_index = index - int(potential_range / 2)
            index = new_index if new_index != index else new_index - 1
            if index < 0:
                index = 0
        return self.resolve(cell, index=index, ceiling=ceiling, floor=floor)

    def _bump_as_too_high(self, index, cell, ceiling, floor):
        "move the index up as as the cell was above/greater-than the last ranged we looked at"
        assert (
            index == floor
        ), "If we`re specified the cell is in a higher range, floor should be set to last index"
        if self.bumped == False and index != self.range_count:
            index = index + 1
            self.bumped = True
        else:
            potential_range = ceiling - floor
            new_index = index + int(potential_range / 2)
            index = new_index if new_index != index else new_index + 1
            if index > self.range_count:
                index = self.range_count
        return self.resolve(cell, index=index, ceiling=ceiling, floor=floor)

    def __confirm_within_bounds(self, cell: Cell):
        """
        Raise an exception if we're trying to resolve a lookup for a
        cell that is out of bounds, making a lookup impossible.

        example: we're trying to resolve a closest relations to the left
        of a cell that is further to the left than any of the ranges we're
        considering.
        """

        err_str = """
                Lookup for observation cell '{cell}' is impossible. No
                cells in your selection exist in direction '{direction}'
                relative to this cell.

                The boundary (furthest cell index) out of the cells you provided
                on the `{axis}` axis has an offset of `{boundary}`.
                """

        out_of_bounds = [
            self.direction.is_upwards and cell.is_above(self.out_of_bounds),
            self.direction.is_downwards and cell.is_below(self.out_of_bounds),
            self.direction.is_left and cell.is_left_of(self.out_of_bounds),
            self.direction.is_right and cell.is_right_of(self.out_of_bounds),
        ]

        if True in out_of_bounds:
            axis = "x" if self.direction._horizontal_axis else "y"
            raise OutOfBoundsError(
                err_str.format(
                    cell=cell,
                    direction=self.direction.is_downwards,
                    axis=axis,
                    boundary=self.out_of_bounds,
                )
            )

    def resolve(self, cell: Cell, index=None, ceiling=None, floor=0) -> Cell:
        """
        Given the cell we want to lookup the relative column value for, use
        a bisection search to identify the correct range in our ordered list of ranges.

        Note - this method is called recursively, using the index kwarg to start
        again at a different point in the list of ranges.
        """

        # If neither the index of ceiling is passed in, then its the
        # very first call - confirm cell is within the bounds and
        # set the defaults
        if ceiling is None or index is None:
            assert ceiling is None
            assert index is None
            ceiling: int = len(self.ranges)
            index: int = self.start_index
            self.__confirm_within_bounds(cell)

        r = self.ranges[index]
        found_it = False

        if self.direction.name in ["above", "up"]:
            if cell.y < r["lowest_offset"]:
                return self._bump_as_too_low(index, cell, ceiling=index, floor=floor)
            elif cell.y > r["highest_offset"]:
                return self._bump_as_too_high(index, cell, ceiling=ceiling, floor=index)
            else:
                found_it = True

        if self.direction.name in ["below", "down"]:
            if cell.y > r["highest_offset"]:
                return self._bump_as_too_high(index, cell, ceiling=ceiling, floor=index)
            elif cell.y < r["lowest_offset"]:
                return self._bump_as_too_low(index, cell, ceiling=index, floor=floor)
            else:
                found_it = True

        if self.direction.name == "left":
            if cell.x < r["lowest_offset"]:
                return self._bump_as_too_low(index, cell, ceiling=index, floor=floor)
            elif cell.x > r["highest_offset"]:
                return self._bump_as_too_high(index, cell, ceiling=ceiling, floor=index)
            else:
                found_it = True

        if self.direction.name == "right":
            if cell.x > r["highest_offset"]:
                return self._bump_as_too_high(index, cell, ceiling=ceiling, floor=index)
            elif cell.x < r["lowest_offset"]:
                return self._bump_as_too_low(index, cell, ceiling=index, floor=floor)
            else:
                found_it = True

        if found_it:
            # cells are implicitly selected right->down-a-row->right as you look at a tabulated
            # (i.e as per standard human reading convention) so we'll cache this index as there's
            # a decent chance the next obs lookup is in the same range
            self.start_index = index

            # this right-then-down-then-right pattern also means that (often, not guaranteed),
            # if the next obs isn't in the last range checked, there's a decent chance it's in a
            # neighbouring range, so we'll "bump" the index once in the relevant direction on a
            # first miss.
            self.bumped = False
            self.index = None

            # Apply str level cell value override if applicable
            return cell
