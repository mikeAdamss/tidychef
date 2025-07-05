"""
Holds the code that defines the local xlsx reader.
"""

import io
from pathlib import Path
from typing import Callable, List, Optional, Union

import requests
import validators
import xlrd

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.acquire.xls.shared import sheets_from_workbook
from tidychef.selection.selectable import Selectable
from tidychef.selection.xls.xls import XlsSelectable
from tidychef.utils.http.caching import get_cached_session


def http(
    source: Union[str, Path],
    selectable: Selectable = XlsSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    session: requests.Session = None,
    cache: bool = True,
    tables: str = None,
    **kwargs,
) -> Union[XlsSelectable, List[XlsSelectable]]:
    """
    Read data from a Path (or string representing a path)
    present on the same machine where tidychef is running.

    This xls reader uses xlrd:
    https://xlrd.readthedocs.io/en/latest/

    Any kwargs passed to this function are propagated to
    the xlrd.open_workbook() method.

    :param source: A url.
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is XlsSelectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of HttpXlsReader.parse() as an argument.
    :param session: An optional requests.Session object.
    :param cache: Boolean flag for whether or not to cache get requests.
    :return: A single populated Selectable of type as specified by selectable param.
    """

    assert validators.url(source), f"'{source}' is not a valid http/https url."

    return acquirer(
        source,
        HttpXlsReader(tables),
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        session=session,
        cache=cache,
        **kwargs,
    )


class HttpXlsReader(BaseReader):
    """
    A reader to lead in a source where that source is a locally
    held xlsx file.
    """

    def parse(
        self,
        source: str,
        selectable: Selectable = XlsSelectable,
        session: requests.Session = None,
        cache: bool = True,
        **kwargs,
    ) -> List[XlsSelectable]:
        """
        Parse the provided source into a list of Selectables. Unless overridden the
        selectable is of type XlsSelectable.

        Additional **kwargs are propagated to xlrd.open_workbook()

        :param source: A url
        :param selectable: The selectable type to be returned.
        :param session: An optional requests.Session object.
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

        bio = io.BytesIO()
        bio.write(response.content)
        bio.seek(0)

        custom_time_formats = kwargs.get("custom_time_formats", {})
        kwargs.pop("custom_time_formats", None)

        workbook: xlrd.Book = xlrd.open_workbook(
            file_contents=bio.read(), formatting_info=True, **kwargs
        )

        sheets = sheets_from_workbook(
            source, selectable, workbook, custom_time_formats, self.tables, **kwargs
        )
        # In this instance we've filtered the tables at the point of reading, so
        # remove the post load table name regex.
        self.tables = None

        if len(sheets) == 1:
            return sheets[0]
        return sheets
