"""
Holds the code that defines the local csv reader.
"""

import csv
from pathlib import Path
from typing import Callable, Optional, Union

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.csv.csv import CsvSelectable
from tidychef.selection.selectable import Selectable
from tidychef.utils import fileutils


def local(
    source: Union[str, Path],
    selectable: Selectable = CsvSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    **kwargs
) -> CsvSelectable:
    """
    Read data from a Path (or string representing a path)
    present on the same machine where tidychef is running.

    This local csv reader uses csv.reader() from the standard
    python library. Keyword arguments passed into this function
    are propagated through to csv.reader().
    https://docs.python.org/3/library/csv.html

    :param source: A Path object or a string representing a path
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is CsvSelectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of LocalCsvReader.parse() as an argument.
    :return: A single populated Selectable of type as specified by selectable param
    """

    return acquirer(
        source,
        LocalCsvReader(),
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs
    )


class LocalCsvReader(BaseReader):
    """
    A reader to lead in a source where that source is a locally
    held csv file.
    """

    def parse(
        self, source: Union[str, Path], selectable: Selectable = CsvSelectable, **kwargs
    ) -> CsvSelectable:
        """
        Parse the provided source into a Selectable. Unless overridden the
        selectable is of type CsvSelectable.

        Optional **kwargs are propagated to the csv.reader() method.

        :param source: A Path or str representing a path indicating a local file
        :param selectable: The selectable type to be returned.
        :return: A list of type as specified by param selectable.
        """

        assert isinstance(
            source, (str, Path)
        ), """
                The source you're passing to acquire.csv.local() needs to
                be either a Path object or a string representing such.
                """

        source: Path = fileutils.ensure_existing_path(source)

        table = Table()
        with open(source, "r", encoding="utf8") as csv_file:
            file_content = csv.reader(csv_file, **kwargs)

            for y_index, row in enumerate(file_content):
                for x_index, cell_value in enumerate(row):
                    table.add_cell(Cell(x=x_index, y=y_index, value=str(cell_value)))

        return selectable(table, source=source)
