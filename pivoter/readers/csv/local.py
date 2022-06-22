import csv
from pathlib import Path

import pivoter.exceptions
from pivoter.models.source.cell import Cell
from pivoter.models.source.table import LiveTable, Table
from pivoter.readers import BaseReader
from pivoter.selection.base import Selectable
from pivoter.selection.csv.csv import CsvInputSelectable


class LocalCsvReader(BaseReader):
    def parse(
        self, delimiter=",", selectable: Selectable = CsvInputSelectable
    ) -> Selectable:
        self._raise_if_source_is_not_path()

        table = Table()
        with open(self.source, "r") as csv_file:
            filecontent = csv.reader(csv_file, delimiter=delimiter)

            for x, row in enumerate(filecontent):
                for y, cell_value in enumerate(row):
                    table.add_cell(Cell(x=x, y=y, value=cell_value))

        live_table = LiveTable.from_table(table)

        return selectable(
            is_singleton_table=True,
            selected_table=live_table,
            had_initial_path=self.source,
            tables=None,
        )
