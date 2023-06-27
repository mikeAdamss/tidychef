"""
Holds the code that defines the local csv reader.
"""

import io
import validators
import copy
import csv
from pathlib import Path
from typing import Any, Callable, Optional, Union

import requests

from datachef.acquire.base import BaseReader
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.selection.csv.csv import CsvInputSelectable
from datachef.selection.selectable import Selectable

from ..base import BaseReader
from ..main import acquirer


def http(
    source: Union[str, Path],
    selectable: Selectable = Selectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    **kwargs
) -> Selectable:
    """
    Read data from a url with the http or https
    scheme.
    """

    assert validators.url(source), f"'{source}' is not a valid http/https url."

    return acquirer(
        source,
        HttpCsvReader,
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs
    )


class HttpCsvReader(BaseReader):
    """
    A reader to lead in a source where that source is a url
    representing a csv.
    """

    def parse(
        source: Any,
        selectable: Selectable = CsvInputSelectable,
        delimiter=",",
        **kwargs
    ) -> Selectable:
        
        response: requests.Response = requests.get(source)
        if not response.ok:
            raise requests.exceptions.HTTPError(f'''
                Unable to get url: {source}
                {response}
                ''')
    
        sio = io.StringIO()
        sio.write(response.text)
        sio.seek(0)
        
        table = Table()
        file_content = csv.reader(sio, delimiter=delimiter, **kwargs)

        for y_index, row in enumerate(file_content):
            for x_index, cell_value in enumerate(row):
                table.add_cell(Cell(x=x_index, y=y_index, value=cell_value))

        return selectable(table, copy.deepcopy(table), source=source)
