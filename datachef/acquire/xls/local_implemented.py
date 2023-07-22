"""
Holds the code that defines the local xlsx reader.
"""

from pathlib import Path
from typing import Callable, List, Optional, Union

import xlrd

from datachef.acquire.base import BaseReader
from datachef.models.source.cell import Cell
from datachef.models.source.table import Table
from datachef.selection.selectable import Selectable
from datachef.selection.xls.xls import XlsSelectable

from ..base import BaseReader
from ..main import acquirer


def local(
    source: Union[str, Path],
    selectable: Selectable = XlsSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    tables: str = None,
    **kwargs,
) -> List[XlsSelectable]:
    """
    Read data from a Path (or string representing a path)
    present on the same machine where datachef is running.

    This xls reader uses xlrd:
    https://xlrd.readthedocs.io/en/latest/

    Any kwargs passed to this function are propagated to
    the xlrd.open_workbook() method.

    :param source: A Path object or a string representing a path
    :param selectable: A class that implements datachef.selection.selectable.Selectable of an inheritor of. Default is XlsSelectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of XlsSelectable.parse() as an argument.
    :return: A single populated Selectable of type as specified by selectable param
    """

    assert isinstance(
        source, (str, Path)
    ), """
        The source you're passing to acquire.csv.local() needs to
        be either a Path object or a string representing such.
        """

    return acquirer(
        source,
        LocalXlsReader(tables),
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
        self,
        source: Union[str, Path],
        selectable: Selectable = XlsSelectable,
        **kwargs,
    ) -> List[XlsSelectable]:
        """
        Parse the provided source into a list of Selectables. Unless overridden the
        selectable is of type XlsSelectable.

        Additional **kwargs are propagated to xlrd.open_workbook()

        :param source: A Path or str representing a path indicating a local file
        :param selectable: The selectable type to be returned.
        :return: A list of type as specified by param selectable.
        """

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
                    table.add_cell(
                        Cell(x=x, y=y, value=str(cell.value) if cell.value else "")
                    )

            datachef_selectables.append(
                selectable(table, source=source, name=worksheet_name)
            )
        return datachef_selectables
