"""
Holds the code that defines the python list_of_lists reader.
"""

from os import linesep
from typing import Callable, List, Optional

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.selectable import Selectable


def pipe_table(
    source: List[List[str]],
    selectable: Selectable = Selectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    **kwargs
) -> Selectable:
    """
    A reader to create a selectable from a string which represents a pipe
    delimited table. this is principally a convenience for testing.

    Example pipe table (without the escapes)

    = \"""
             |        |
        Male | Female | Both
        4    | 5      | 6
        7    | 8      | 9
      \"""

    :param source: A str representing a pipe table
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is Selectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of ListOfListsReader.parse() as an argument.
    :return: A single populated Selectable of type as specified by selectable param
    """
    return acquirer(
        source,
        PipeTableReader(),
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs
    )


class PipeTableReader(BaseReader):
    def parse(self, source: str, selectable: Selectable = Selectable) -> Selectable:
        """
        Parse the provided source into a list of Selectables. Unless overridden the
        selectable is of type XlsSelectable.

        Additional **kwargs are propagated to xlrd.open_workbook()

        :param source: A list of lists of strings representing rows of cells
        :param selectable: The selectable type to be returned.
        :return: A populated instance of type as specified by param selectable.
        """
        table = Table()

        raw_rows = source.split(linesep)
        rows = []
        row_cell_count = None

        for row in raw_rows:
            if len(row.strip()) == 0:
                continue
            row_cells = [x.strip() for x in row.split("|")]
            if row_cell_count is None:
                row_cell_count = len(row_cells)
            else:
                assert (
                    len(row_cells) == row_cell_count
                ), "All rows in a pipe table must be the same length"
            rows.append(row_cells)

        for y_index, row in enumerate(rows):
            for x_index, cell_value in enumerate(row):
                table.add_cell(Cell(x=x_index, y=y_index, value=cell_value))

        return selectable(table)
