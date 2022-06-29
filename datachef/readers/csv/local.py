import csv

from datachef.models.source.cell import Cell
from datachef.models.source.table import LiveTable, Table
from datachef.readers.base import BaseReader
from datachef.selection.csv.csv import CsvInputSelectable
from datachef.selection.selectable import Selectable


class LocalCsvReader(BaseReader):
    def parse(
        self, delimiter=",", selectable: Selectable = CsvInputSelectable
    ) -> Selectable:
        self._raise_if_source_is_not_path()

        table = Table()
        with open(self.source, "r") as csv_file:
            filecontent = csv.reader(csv_file, delimiter=delimiter)

            for y, row in enumerate(filecontent):
                for x, cell_value in enumerate(row):
                    table.add_cell(Cell(x=x, y=y, value=cell_value))

        live_table = LiveTable.from_table(table)

        return selectable(
            is_singleton_table=True,
            selected_table=live_table,
            had_initial_path=self.source,
            tables=None,
        )
