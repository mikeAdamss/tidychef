"""
Holds and defines the reader for create a selection from a list of lists
"""
import copy
from typing import Any

from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.acquire.base import BaseReader
from datachef.selection.selectable import Selectable



from dataclasses import dataclass
from ..base import BaseReader
from typing import Any, Optional, Callable, Union
from pathlib import Path

from datachef.selection.selectable import Selectable
from datachef.utils import fileutils

from ..acquirer import acquirer


def list_of_lists(source: Union[str, Path],
                selectable: Selectable = Selectable,
                pre_hook:Optional[Callable] = None,
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
        source, ListOfListsReader,
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
                table.add_cell(Cell(x=x_index, y=y_index, value=cell_value))

        return selectable(table, copy.deepcopy(table))
