"""
Holds the code that defines the local xlsx reader.
"""

from pathlib import Path
from typing import Callable, List, Optional, Union

import xlrd

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.acquire.xls.shared import sheets_from_workbook
from tidychef.selection.selectable import Selectable
from tidychef.selection.xls.xls import XlsSelectable


def local(
    source: Union[str, Path],
    selectable: Selectable = XlsSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
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

    :param source: A Path object or a string representing a path
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is XlsSelectable
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

        custom_time_formats = kwargs.get("custom_time_formats", {})
        kwargs.pop("custom_time_formats", None)

        workbook: xlrd.Book = xlrd.open_workbook(source, formatting_info=True)

        sheets = sheets_from_workbook(
            source, selectable, workbook, custom_time_formats, self.tables, **kwargs
        )

        # In this instance we've filtered the tables at the point of reading, so
        # remove the post load filter.
        self.tables = None

        if len(sheets) == 1:
            return sheets[0]
        return sheets
