"""
Holds and defines the local csv reader class.
"""

import copy
import csv

from datachef.models.source.cell import Cell
from datachef.models.source.table import LiveTable, Table
from datachef.readers.base import BaseReader
from datachef.selection.csv.csv import CsvInputSelectable
from datachef.selection.selectable import Selectable


class LocalCsvReader(BaseReader):
    """
    A reader to lead in a source where that source is a locally
    held csv file.
    """

    def parse(
        self, delimiter=",", selectable: Selectable = CsvInputSelectable
    ) -> Selectable:
        self._raise_if_source_is_not_path()

        table = Table()
        with open(self.source, "r", encoding="utf8") as csv_file:
            filecontent = csv.reader(csv_file, delimiter=delimiter)

            for y_index, row in enumerate(filecontent):
                for x_index, cell_value in enumerate(row):
                    table.add_cell(Cell(x=x_index, y=y_index, value=cell_value))

        return selectable(
            table, copy.deepcopy(table), source=self.source
        )
