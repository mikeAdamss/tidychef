"""
Holds the code that defines the local xlsx reader.
"""

import copy
import io
from pathlib import Path
from typing import Any, Callable, List, Optional, Union

import xlrd

from datachef.acquire.base import BaseReader
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.selection.selectable import Selectable
from datachef.selection.xls.xls import XlsSelectable
from datachef.utils.http.caching import get_cached_session

from ..base import BaseReader
from ..main import acquirer


def local(
    source: Union[str, Path],
    selectable: Selectable = XlsSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
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
        LocalXlsReader,
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs,
    )


class LocalXlsReader(BaseReader):
    """
    A reader to lead in a source where that source is a locally
    held xls file.
    """

    def parse(
        source: Any,
        selectable: Selectable = XlsSelectable,
        **kwargs,
    ) -> List[XlsSelectable]:

        workbook: xlrd.Book = xlrd.open_workbook(source)
        assert isinstance(workbook, xlrd.Book)

        datachef_selectables = []
        worksheet_names = workbook.sheet_names()
        for worksheet_name in worksheet_names:

            worksheet = workbook.sheet_by_name(worksheet_name, **kwargs)

            table = Table()
            num_rows = worksheet.nrows
            for y in range(0, num_rows):
                for x, cell in enumerate(worksheet.row(y)):
                    table.add_cell(Cell(x=x, y=y, value=str(cell.value) if cell.value else ""))

            datachef_selectables.append(
                selectable(
                    table, copy.deepcopy(table), source=source, _name=worksheet_name
                )
            )
        return datachef_selectables
