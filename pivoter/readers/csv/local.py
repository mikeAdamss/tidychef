import csv
from pathlib import Path

import pivoter.exceptions
from pivoter.models.source.table import LiveTable
from pivoter.readers import BaseReader
from pivoter.models.source.cell import Cell
from pivoter.models.source.input import BaseInput
from pivoter.models.source.table import LiveTable, Table
from pivoter.selection.csv.csv import CsvInputSelectable


class LocalCsvReader(BaseReader):
    def parse(self, delimiter=",") -> BaseInput:

        if not isinstance(self.source, Path):
            raise pivoter.exceptions.FileInputError(
                "A local csv input should be provided in the form of a pathlib.Path"
            )

        table = Table()
        with open(self.source, "r") as csv_file:
            filecontent = csv.reader(csv_file, delimiter=delimiter)

            for x, row in enumerate(filecontent):
                for y, cell_value in enumerate(row):
                    table.add_cell(Cell(x=x, y=y, value=cell_value))

        live_table = LiveTable.from_table(table)

        return CsvInputSelectable(
            is_singleton_table=True,
            selected_table=live_table,
            had_initial_path=self.source,
            tables=None,
        )
