"""
Holds and defines the local csv reader class.
"""

import copy
import csv
from pathlib import Path
from typing import Any

from datachef.utils import fileutils
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.acquire.base import BaseReader
from datachef.selection.csv.csv import CsvInputSelectable
from datachef.selection.selectable import Selectable


from dataclasses import dataclass
from ..base import BaseReader
from typing import Any, Optional, Callable, Union
from pathlib import Path

from datachef.selection.selectable import Selectable
from datachef.utils import fileutils

from ..acquirer import acquirer



def local(source: Union[str, Path],
                selectable: Selectable = Selectable,
                pre_hook:Optional[Callable] = None,
                post_hook: Optional[Callable] = None,
                **kwargs
                ) -> Selectable:
    """
    Read data from a Path (or string representing a path)
    present on the same machine where datachef is running.

    This local csv reader uses csv.reader() from the standard
    python library. Keyword arguments passed into this function
    are propogated through to csv.reader().
    https://docs.python.org/3/library/csv.html
    """

    # Ensure that what has been passed in is or can be a Path
    # object and that the file exists.
    source_path: Path = fileutils.ensure_existing_path(source)

    return acquirer(
        source_path, LocalCsvReader,
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
        source: Any, selectable: Selectable = CsvInputSelectable, delimiter=",", **kwargs
    ) -> Selectable:
        table = Table()
        with open(source, "r", encoding="utf8") as csv_file:
            file_content = csv.reader(csv_file, delimiter=delimiter, **kwargs)

            for y_index, row in enumerate(file_content):
                for x_index, cell_value in enumerate(row):
                    table.add_cell(Cell(x=x_index, y=y_index, value=cell_value))

        return selectable(table, copy.deepcopy(table), source=source)
