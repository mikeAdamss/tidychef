import csv
from pathlib import Path

import pivoter.exceptions
from pivoter.readers import BaseReader
from pivoter.models.source import Cell, Input, Table, input_from_single_table


class LocalCsvReader(BaseReader):
    def parse(self, delimiter=",") -> Input:

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

        return input_from_single_table(self.source, table)
