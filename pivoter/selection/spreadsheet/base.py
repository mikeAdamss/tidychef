import copy
import logging
from typing import List

from pivoter.models.source.cell import BaseCell
from pivoter.utils import cellutils

from .. import datafuncs as dfc
from ..base import Selectable


class BaseSpreadsheetSelectable(Selectable):
    """
    Class representing a spreadsheet input, holding
    all methods commmon to spreadsheets of whatever
    flavour.
    """

    def excel_ref(self, excel_ref: str):
        """
        Selects just the cells as indicated by the provided excel reference,
        "A6", "B17:B24": etc.
        """

        if ":" in excel_ref:
            wanted: List[BaseCell] = cellutils.multi_excel_ref_to_basecells(excel_ref)
        else:
            wanted: BaseCell = cellutils.single_excel_ref_to_basecells(excel_ref)
            wanted = [wanted]

        selected = dfc.exactly_matched_xy_cells(self.cells, wanted)
        logging.warning(
            f"excel ref input {excel_ref}, results in cells {dfc.xycells_to_excel_ref(self.cells)}"
        )

        return_self = copy.deepcopy(self)
        return_self.cells = selected
        return return_self
