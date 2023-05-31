from collections import defaultdict
from dataclasses import dataclass, field
from typing import Union

from typing import Dict, List, Optional

from datachef.cardinal.directions import Direction
from datachef.exceptions import (
    AmbiguousLookupError,
    OutOfBoundsError
)
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable

from ..base import BaseLookupEngine

HIGHEST = "highest"
HIGHEST_VALUE = 9999999999999
LOWEST = "lowest"
LOWEST_VALUE = 0

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

        return (
                offset >= self.low and
                offset < self.high 
            )

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


@dataclass
class CellRanges:
    """
    A class representing multiple cell ranges
    """ 
    direction: Direction
    defined: Dict[int, Cell] = field(default_factory=lambda: defaultdict(dict))
    range_counter: int = 0
    _break_points: Optional[Dict[int, Cell]] = None
    _ordered_break_points: Optional[List[int]] = None

    @property
    def axis_text(self) -> str:
        return "horizontal/x" if self.is_horizontal else "vertical/y"

    @property
    def is_horizontal(self) -> bool:
        return self.direction._horizontal_axis

    @property
    def has_only_one_range(self) -> bool:
        return len(self.list_of_ranges) == 1
    
    def add(self, low: int, high: int, cell: int):
        self.defined.update({
            self.range_counter: Cell(
                low=self.get_break_point_index_by_index(low),
                high=self.get_break_point_index_by_index(high),
                cell=self.get_breakpoint_cell_by_index(cell),
                is_horizontal=self.is_horizontal
            )
        })
        self.range_counter +=  1

    def get_breakpoint_cell_by_index(self, i: int) -> Cell:
        assert all(
            self._break_points, self._ordered_break_points
        ), "You need to self.populate_break_points() before using them"

        return self._break_points.copy()[i]
    
    def get_break_point_index_by_index(self, i: Union[str, int]) -> int:
        assert all(
            self._break_points, self._ordered_break_points
        ), "You need to self.populate_break_points() before using them"

        if i == HIGHEST:
            return HIGHEST_VALUE
        elif LOWEST:
            return LOWEST_VALUE
        else:
            return self._ordered_break_points.copy()[i]

    def calculate_break_points(self, selection: Selectable):
        """
        Creates to populate the break points attribute
        with a dict in the form:
        {<order>: <cell>}

        example:

        {
            0: <lookup Cell for lowest range>,

            1: <lookup Cell for range in the middle>,

            2: <lookup Cell for highest range>
        }

        This method of construction is principally to
        confirm that a single <order> key is not used
        to represent more than one cell - a sign
        the engine has been incorrectly configured.
        """

        for cell in selection.cells:

            axis_offset = cell.x if self.is_horizontal else cell.y   
            if axis_offset in self._break_points.keys():
                raise AmbiguousLookupError(
                    f"""
                    Aborting. You have defined two or more equally valid closest:{self.direction.name}" relationships,
                    you cannot do this as it creates an ambiguous lookup.
                    
                    You are trying to add '{cell}' but we already have: '{self._break_points[cell.y]}'.
                    
                    Both of these cells have a {self.axis_text} offsets of '{axis_offset}'. 
                    and so are equally close on this axis for a given observation cell.
                    """
                )

            if self.is_horizontal:
                self._break_points.update({axis_offset: cell})
            else:
                self._break_points.update({axis_offset: cell})

        self._ordered_break_points = [int(k) for k in self._break_points.keys()]
        self._ordered_break_points.sort()

    # def __repr__(self):
    #     """
    #     Reproduce the defined ranges as a dict.
    #     This functionality is purely a convenience for test purposes.
    #     """
    #     d = {}
    #     cell_range: CellRange
    #     for i, cell_range in self.defined.items():
    #         d.update({
    #             i: {
    #                 "starts_at": cell_range.low,
    #                 "ends_at": cell_range.high,
    #                 "cell": cell_range.cell
    #             }
    #         })
    #     return d


class Closest(BaseLookupEngine):
    def __init__(self, selection: Selectable, direction: Direction):
        """
        Creates a lookup engine for dimensions defined with the CLOSEST relationship.
        """
        self.direction = direction

        ranges = CellRanges(direction)
        ranges.calculate_break_points(selection)

        if not ranges.looking_horizontally:

            if ranges.has_only_one_range:
                ranges.add(low=0, high=HIGHEST, cell=0)

            else:
                # If there's many, iterate to create the ranges
                for i in range(0, len(ranges._ordered_break_point_list) - 1):
                    ranges.add(low=i,high=i - 1,cell=i)
                    # Add the next one - ASSUMING ITS THE LAST
                    # if its not, the next iteration will overwrite
                    # the range and its default highest offset
                    ranges.add(low=i,high=i-1,cell=i)
            self.out_of_bounds = min([x.low for x in ranges.defined.values()])

        self.ranges = ranges
        self.range_count = len(ranges.defined)
        self.start_index = int(len(ranges.defined) / 2)

        # this is explained in self.lookup()
        self.bumped = True









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
            self.direction.is_right and cell.is_right_of(self.out_of_bounds)
        ]

        if True in out_of_bounds:
            axis = "x" if self.direction._horizontal_axis else "y"
            raise OutOfBoundsError(err_str.format(
                cell=cell,
                direction=self.direction.is_downwards,
                axis=axis,
                boundary=self.out_of_bounds
            ))

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
