"""
Holds the code that defines the local csv reader.
"""

import copy
import csv
import io
from pathlib import Path
from typing import Any, Callable, Optional, Union

import requests
import validators

from datachef.acquire.base import BaseReader
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.selection.csv.csv import CsvSelectable
from datachef.selection.selectable import Selectable
from datachef.utils.http.caching import get_cached_session

from ..base import BaseReader
from ..main import acquirer


def http(
    source: Union[str, Path],
    selectable: Selectable = CsvSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    session: requests.Session = None,
    cache: bool = True,
    **kwargs,
) -> CsvSelectable:
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
        session=session,
        cache=cache,
        **kwargs,
    )


class HttpCsvReader(BaseReader):
    """
    A reader to lead in a source where that source is a url
    representing a csv.
    """

    def parse(
        source: Any,
        selectable: Selectable = CsvSelectable,
        delimiter=",",
        session: requests.Session = None,
        cache: bool = True,
        **kwargs,
    ) -> CsvSelectable:

        if not session:
            if cache:
                session = get_cached_session()
            else:
                session = requests.session()

        response: requests.Response = session.get(source)
        if not response.ok:
            raise requests.exceptions.HTTPError(
                f"""
                Unable to get url: {source}
                {response}
                """
            )

        sio = io.StringIO()
        sio.write(response.text)
        sio.seek(0)

        table = Table()
        file_content = csv.reader(sio, delimiter=delimiter, **kwargs)

        for y_index, row in enumerate(file_content):
            for x_index, cell_value in enumerate(row):
                table.add_cell(Cell(x=x_index, y=y_index, value=cell_value))

        return selectable(table, copy.deepcopy(table), source=source)
