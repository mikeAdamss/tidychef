import json
from typing import List

from datachef.cardinal.directions import BaseDirection, Direction
from datachef.exceptions import (
    FailedLookupError,
    MissingDirectLookupError,
    OutOfBoundsError,
    UnknownDirectionError,
)
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable

from ..base import BaseLookupEngine


class Closest(BaseLookupEngine):
    def __init__(self, selection: Selectable, direction: Direction):
        """
        Creates a lookup engine for dimensions defined with the CLOSEST relationship.
        """
        self.direction = direction

        # the break-point is the start/end of a range. Effectively the index of the cell
        # along the relevant axis.
        break_points = {}
        for cell in selection.cells:

            axis_offset = cell.y if not direction._horizontal_axis else cell.x
            if axis_offset in break_points.keys():
                break_points_as_str = json.dumps(break_points, default=lambda x: str(x))
                raise Exception(
                    f"""
                    Aborting. You have defined two or more equally valid closest:{direction.name}" relationships.
                    Trying to add {axis_offset}:{cell} but we already have: {break_points_as_str}
                        """
                )

            if not direction._horizontal_axis:
                break_points.update({cell.y: cell})
            else:
                break_points.update({cell.x: cell})

        ordered_break_point_list = [int(k) for k in break_points.keys()]
        ordered_break_point_list.sort()

        # TODO - explain and document this
        ranges = {}
        if direction._horizontal_axis:
            x = 0

            # If it's a single cell selection, we only need a single range
            if len(ordered_break_point_list) == 1:
                ranges.update(
                    {
                        0: {
                            "lowest_offset": ordered_break_point_list.copy()[0],
                            "highest_offset": 99999999999,
                            "cell": break_points[ordered_break_point_list.copy()[0]],
                        }
                    }
                )
            else:
                # If there's many, iterate to create the ranges
                for i in range(0, len(ordered_break_point_list) - 1):
                    ranges.update(
                        {
                            x: {
                                "lowest_offset": ordered_break_point_list.copy()[i],
                                "highest_offset": ordered_break_point_list.copy()[i + 1]
                                - 1,
                                "cell": break_points[
                                    ordered_break_point_list.copy()[i]
                                ],
                            }
                        }
                    )
                    x += 1
                    ranges.update(
                        {
                            x: {
                                "lowest_offset": ordered_break_point_list.copy()[-1],
                                "highest_offset": 99999999999,
                                "cell": break_points[
                                    ordered_break_point_list.copy()[-1]
                                ],
                            }
                        }
                    )
            self.out_of_bounds = min([x["lowest_offset"] for x in ranges.values()])
        else:
            x = 0
            ranges.update(
                {
                    0: {
                        "lowest_offset": 0,
                        "highest_offset": ordered_break_point_list.copy()[0],
                        "cell": break_points[ordered_break_point_list.copy()[0]],
                    }
                }
            )
            x = 1
            for i in range(1, len(ordered_break_point_list)):
                ranges.update(
                    {
                        x: {
                            "lowest_offset": ordered_break_point_list.copy()[i - 1] + 1,
                            "highest_offset": ordered_break_point_list.copy()[i],
                            "cell": break_points[ordered_break_point_list.copy()[i]],
                        }
                    }
                )
                x += 1
            self.out_of_bounds = max([x["highest_offset"] for x in ranges.values()])

        self.ranges = ranges
        self.range_count = len(ranges)  # do this here, so we only do it once
        self.start_index = int(len(ranges) / 2)

        # this is explained in self.lookup()
        self.bumped = True

        # track the correct one
        self.found_cell = None

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
        return self.lookup(cell, index=index, ceiling=ceiling, floor=floor)

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
        return self.lookup(cell, index=index, ceiling=ceiling, floor=floor)

    def lookup(self, cell, index=None, ceiling=None, floor=0):
        """
        Given the cell we want to lookup the relative column value for, use
        a bisection search to identify the correct range in our ordered list of ranges.

        Note - this method is called recursively, using the index kwarg to start
        again at a different point in the list of ranges.
        """
        ceiling = len(self.ranges) if ceiling is None else ceiling

        found_it = False

        if index == None:
            index = self.start_index

        # Blowup early if the cell is out of bounds
        # (eg to the left of the leftmost left lookup - no viable lookup)
        msg = f"""
            Lookup for cell "{cell}" is impossible. No selected values for dimension "{self.label}"
            exist in the {self.direction.name} direction from this cell"""
        switch = [
            self.direction.name in ["above", "up"] and cell.y < self.out_of_bounds,
            self.direction == "left" and cell.x < self.out_of_bounds,
            self.direction in ["below", "down"] and cell.y > self.out_of_bounds,
            self.direction == "right" and cell.x > self.out_of_bounds,
        ]
        if True in switch:
            raise OutOfBoundsError(msg)

        r = self.ranges[index]

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
            # cells are implicitly selected right->down-a-row->right as you look at a spreadsheet
            # so we'll cache this index as there's a decent chance the next obs lookup is in the same range
            self.start_index = index

            # this right-then-down-then-right pattern also means that (often, not guaranteed),
            # if the next obs isn't in the last range checked, there's a decent chance it's in a
            # neighbouring range, so we'll "bump" the index once in the relevant direction on a
            # first miss.
            self.bumped = False
            self.index = None

            # Apply str level cell value override if applicable
            return cell
