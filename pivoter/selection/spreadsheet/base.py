from typing import List

from pivoter.models.source.cell import BaseCell
from pivoter.utils import cellutils
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

        selected = self.datamethods._exactly_matched_xy_cells(self.cells, wanted)

        self.selected_table.filtered.cells = selected
        return self
