"""
Holds the code that defines the local xlsx reader.
"""

import copy
import io
from pathlib import Path
from typing import Any, Callable, Optional, Union, List

import openpyxl
import requests

from datachef.acquire.base import BaseReader
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.selection.xlsx.xlsx import XlsxInputSelectable
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
        HttpXlsxReader,
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs
    )


class HttpXlsxReader(BaseReader):
    """
    A reader to lead in a source where that source is a locally
    held xlsx file.
    """

    def parse(
        source: Any,
        selectable: Selectable = XlsxInputSelectable,
        data_only=True,
        **kwargs
    ) -> List[Selectable]:

        response: requests.Response = requests.get(source)
        if not response.ok:
            raise requests.exceptions.HTTPError(f'''
                Unable to get url: {source}
                {response}
                ''')
    
        sio = io.StringIO()
        sio.write(response.text)
        sio.seek(0)

        workbook: openpyxl.Workbook = openpyxl.load_workbook(sio, data_only=data_only)

        datachef_selectables = []
        worksheet_names = workbook.get_sheet_names()
        for worksheet_name in worksheet_names:

            worksheet = workbook.get_sheet_by_name(worksheet_name)

            table = Table()
            for y, row in enumerate(worksheet.iter_rows()):
                for x, cell in enumerate(row):
                        table.add_cell(Cell(x=x, y=y, value=cell.value))

            datachef_selectables.append(selectable(table, copy.deepcopy(table),
                                                   source=source, _name=worksheet_name))
        return datachef_selectables