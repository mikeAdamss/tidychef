"""
Holds the code that defines the python list_of_lists reader.
"""
import copy
from pathlib import Path
from typing import Callable, Optional, Union

from datachef.acquire.base import BaseReader
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.selection.selectable import Selectable

from ..base import BaseReader
from ..main import acquirer


def list_of_lists(
    source: Union[str, Path],
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
    """
    return acquirer(
        source,
        ListOfListsReader,
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs
    )


class ListOfListsReader(BaseReader):
    def parse(source, selectable: Selectable = Selectable) -> Selectable:
        table = Table()

        for y_index, row in enumerate(source):
            for x_index, cell_value in enumerate(row):
                table.add_cell(Cell(x=x_index, y=y_index, value=str(cell_value)))

        return selectable(table, copy.deepcopy(table))
