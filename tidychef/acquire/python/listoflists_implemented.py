"""
Holds the code that defines the python list_of_lists reader.
"""

from typing import Callable, List, Optional

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.selectable import Selectable


def list_of_lists(
    source: List[List[str]],
    selectable: Selectable = Selectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    **kwargs
) -> Selectable:
    """
    A reader to create a selectable from a list of python
    lists, with each cell entry being a simple string.

    Regarding ordering we traverse the x axis then the y axis,
    i.e standard human reading order.

    For example:
    [
        ["Content of A1", "Contents of B1", "Contents of C1"],
        ["Content of A2", "Contents of B2", "Contents of C2"]
    ]

    :param source: A python list of lists
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is Selectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of ListOfListsReader.parse() as an argument.
    :return: A single populated Selectable of type as specified by selectable param
    """
    return acquirer(
        source,
        ListOfListsReader(),
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs
    )


class ListOfListsReader(BaseReader):
    def parse(self, source, selectable: Selectable = Selectable) -> Selectable:
        """
        Parse the provided source into a list of Selectables. Unless overridden the
        selectable is of type XlsSelectable.

        Additional **kwargs are propagated to xlrd.open_workbook()

        :param source: A list of lists of strings representing rows of cells
        :param selectable: The selectable type to be returned.
        :return: A populated instance of type as specified by param selectable.
        """
        table = Table()

        assert (
            len(set([len(x) for x in source])) == 1
        ), "All rows must be the same length"

        for y_index, row in enumerate(source):
            for x_index, cell_value in enumerate(row):
                table.add_cell(Cell(x=x_index, y=y_index, value=str(cell_value)))

        return selectable(table)
