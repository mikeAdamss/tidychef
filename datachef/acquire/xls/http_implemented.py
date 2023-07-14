"""
Holds the code that defines the local xlsx reader.
"""

import io
from pathlib import Path
from typing import Callable, List, Optional, Union

import requests
import validators
import xlrd

from datachef.acquire.base import BaseReader
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.selection.selectable import Selectable
from datachef.selection.xls.xls import XlsSelectable
from datachef.utils.http.caching import get_cached_session

from ..base import BaseReader
from ..main import acquirer


def http(
    source: Union[str, Path],
    selectable: Selectable = XlsSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    session: requests.Session = None,
    cache: bool = True,
    **kwargs,
) -> List[XlsSelectable]:
    """
    Read data from a Path (or string representing a path)
    present on the same machine where datachef is running.

    This xls reader uses xlrd:
    https://xlrd.readthedocs.io/en/latest/

    Any kwargs passed to this function are propagated to
    the xlrd.open_workbook() method.

    :param source: A url.
    :param selectable: A class that implements datachef.selection.selectable.Selectable of an inheritor of. Default is XlsSelectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of HttpXlsReader.parse() as an argument.
    :param session: An optional requests.Session object.
    :param cache: Boolean flag for whether or not to cache get requests.
    :return: A single populated Selectable of type as specified by selectable param.
    """

    assert validators.url(source), f"'{source}' is not a valid http/https url."

    return acquirer(
        source,
        HttpXlsReader,
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

        workbook: xlrd.Book = xlrd.open_workbook(file_contents=bio.read(), **kwargs)
        assert isinstance(workbook, xlrd.Book)

        datachef_selectables = []
        worksheet_names = workbook.sheet_names()
        for worksheet_name in worksheet_names:

            worksheet = workbook.sheet_by_name(worksheet_name, **kwargs)

            table = Table()
            num_rows = worksheet.nrows
            for y in range(0, num_rows):
                for x, cell in enumerate(worksheet.row(y)):
                    table.add_cell(
                        Cell(x=x, y=y, value=str(cell.value) if cell.value else "")
                    )

            datachef_selectables.append(
                selectable(table, source=source, name=worksheet_name)
            )
        return datachef_selectables
