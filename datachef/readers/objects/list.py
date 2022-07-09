"""
Holds and defines the reader for create a selection from a list of lists
"""
import copy

from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.readers.base import BaseReader
from datachef.selection.selectable import Selectable


class ListReader(BaseReader):
    """
    A reader to create a selectable from a python list object.

    For example:
    [
        [A1, B1, C1],
        [A2, B2, C2]
    ]
    """

    def parse(self, selectable: Selectable = Selectable) -> Selectable:
        table = Table()

        for y_index, row in enumerate(self.source):
            for x_index, cell_value in enumerate(row):
                table.add_cell(Cell(x=x_index, y=y_index, value=cell_value))

        return selectable(table, copy.deepcopy(table))
