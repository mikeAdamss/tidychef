"""
Holds the code that defines the local xlsx reader.
"""

import copy
import io
from pathlib import Path
from typing import Any, Callable, List, Optional, Union

import xlrd
import requests

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

    This local xlsx reader uses openpyxl:
    https://openpyxl.readthedocs.io/en/stable/index.html

    Any kwargs passed to this function are propogated to
    the openpyxl.load_workbook() method
    """

    assert isinstance(
        source, (str, Path)
    ), """
        The source you're passing to acquire.csv.local() needs to
        be either a Path object or a string representing such.
        """

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
        source: Any,
        selectable: Selectable = XlsSelectable,
        session: requests.Session = None,
        cache: bool = True,
        **kwargs,
    ) -> List[XlsSelectable]:

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

        workbook: xlrd.Book = xlrd.open_workbook(file_contents=bio.read())
        assert isinstance(workbook, xlrd.Book)

        datachef_selectables = []
        worksheet_names = workbook.sheet_names()
        for worksheet_name in worksheet_names:

            worksheet = workbook.sheet_by_name(worksheet_name, **kwargs)

            table = Table()
            num_rows = worksheet.nrows
            for y in range(0, num_rows):
                for x, cell in enumerate(worksheet.row(y)):
                    table.add_cell(Cell(x=x, y=y, value=cell.value if cell.value else ""))

            datachef_selectables.append(
                selectable(
                    table, copy.deepcopy(table), source=source, _name=worksheet_name
                )
            )
        return datachef_selectables
