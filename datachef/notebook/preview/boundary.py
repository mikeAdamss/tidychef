from typing import Dict, List, Union

from datachef.exceptions import PreviewBoundarySpecificationError
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable


class Boundary:
    """
    Class to calculate and help manage the boundary of
    the cells we wish to display in this preview.
    """

    def __init__(
        self,
        selections: List[Selectable],
        bounded: Union[str, Dict[str, str]] = None,
    ):

        self.bounded = bounded
        if bounded is None:
            pcells = selections[0].pcells
            self.max_selected_x: int = dfc.maximum_x_offset(pcells)
            self.max_selected_y: int = dfc.maximum_y_offset(pcells)
            self.min_selected_x: int = dfc.minimum_x_offset(pcells)
            self.min_selected_y: int = dfc.minimum_y_offset(pcells)

        else:
            bad_bounded_arg = False
            if isinstance(bounded, str):
                cells_wanted = dfc.multi_excel_ref_to_basecells(bounded)
                (
                    self.min_selected_x,
                    self.max_selected_x,
                    self.min_selected_y,
                    self.max_selected_y,
                ) = dfc.get_outlier_indicies(cells_wanted)
            else:
                if not isinstance(bounded, dict):
                    bad_bounded_arg = True
                else:
                    if (
                        "start_xy" not in bounded.keys()
                        or "end_xy" not in bounded.keys()
                    ):
                        bad_bounded_arg = True
                    else:
                        if (
                            "," not in bounded["start_xy"]
                            or "," not in bounded["end_xy"]
                        ):
                            bad_bounded_arg = True
                        else:
                            if any(
                                [
                                    not bounded["start_xy"].split(",")[0].isnumeric(),
                                    not bounded["start_xy"].split(",")[1].isnumeric(),
                                    not bounded["end_xy"].split(",")[0].isnumeric(),
                                    not bounded["end_xy"].split(",")[1].isnumeric(),
                                ]
                            ):
                                bad_bounded_arg = True
                            else:
                                if int(bounded["start_xy"].split(",")[0]) > int(
                                    bounded["end_xy"].split(",")[0]
                                ) or int(bounded["start_xy"].split(",")[1]) > int(
                                    bounded["end_xy"].split(",")[1]
                                ):
                                    bad_bounded_arg = True

                if bad_bounded_arg:
                    raise PreviewBoundarySpecificationError(
                        """
                        You have provided incorrect arguments for the boundary= keyword.

                        Valid arguments are:
                        An multicell excel style reference, i.e A1:C5
                        
                        Or a dictionary in the form:
                        {"start_xy": "<startx>,<starty>", "end_xy": "<endx>,<endy>"}

                        Example (for A1:C5)
                        {"start_xy": "0,0", "end_xy": "2,4"}
                    """
                    )

                self.min_selected_x = int(bounded["start_xy"].split(",")[0])
                self.max_selected_x = int(bounded["end_xy"].split(",")[0])
                self.min_selected_y = int(bounded["start_xy"].split(",")[1])
                self.max_selected_y = int(bounded["end_xy"].split(",")[1])

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
