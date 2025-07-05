"""
Holds the code that defines the local csv reader.
"""

import csv
import io
from typing import Any, Callable, Optional

import requests
import validators

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.csv.csv import CsvSelectable
from tidychef.selection.selectable import Selectable
from tidychef.utils.http.caching import get_cached_session


def http(
    source: str,
    selectable: Selectable = CsvSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    session: requests.Session = None,
    cache: bool = True,
    **kwargs,
) -> CsvSelectable:
    """
    Creates a selectable with default child class CsvSelectable from
    a url with the http or https scheme.

    :param source: A url.
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is CsvSelectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of HttpCsvReader.parse() as an argument.
    :param session: An optional requests.Session object.
    :param cache: Boolean flag for whether or not to cache get requests.
    :return: A single populated Selectable of type as specified by selectable param.
    """

    assert validators.url(source), f"'{source}' is not a valid http/https url."

    return acquirer(
        source,
        HttpCsvReader(),
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        session=session,
        cache=cache,
        **kwargs,
    )


class HttpCsvReader(BaseReader):
    """
    A reader to read in a source where that source is a url
    representing a csv.
    """

    def parse(
        self,
        source: Any,
        selectable: Selectable = CsvSelectable,
        session: requests.Session = None,
        cache: bool = True,
        **kwargs,
    ) -> CsvSelectable:
        """
        Parse the provided source into a Selectable. Unless overridden the
        selectable is of type CsvSelectable.

        Optional **kwargs are propagated to the csv.reader() method.

        :param source: A url
        :param selectable: The selectable type to be returned.
        :param session: An optional requests.Session object.
        :param cache: Boolean flag for whether or not to cache get requests.
        :return: A list of type as specified by param selectable.
        """

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
        file_content = csv.reader(sio, **kwargs)

        for y_index, row in enumerate(file_content):
            for x_index, cell_value in enumerate(row):
                table.add_cell(Cell(x=x_index, y=y_index, value=str(cell_value)))

        return selectable(table, source=source)
