"""
Holds the code that defines the local xlsx reader.
"""

from pathlib import Path
from typing import Callable, List, Optional, Union

import ezodf
from ezodf.document import PackagedDocument

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.ods.ods import OdsSelectable
from tidychef.selection.selectable import Selectable


def local(
    source: Union[str, Path],
    selectable: Selectable = OdsSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    tables: str = None,
    **kwargs,
) -> Union[OdsSelectable, List[OdsSelectable]]:
    """
    Read data from a Path (or string representing a path)
    present on the same machine where tidychef is running.

    :param source: A Path object or a string representing a path
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is XlsSelectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of LocalOdsReader.parse() as an argument.
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
        LocalOdsReader(tables),
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        **kwargs,
    )


class LocalOdsReader(BaseReader):
    """
    A reader to lead in a source where that source is a locally
    held xls file.
    """

    def parse(
        self,
        source: Union[str, Path],
        selectable: Selectable = OdsSelectable,
        **kwargs,
    ) -> Union[OdsSelectable, List[OdsSelectable]]:
        """
        Parse the provided source into a list of OdsSelectable. Unless overridden the
        selectable is of type OdsSelectable.

        :param source: A Path or str representing a path indicating a local file
        :param selectable: The selectable type to be returned.
        :return: A list of type as specified by param selectable.
        """

        spreadsheet: PackagedDocument = ezodf.opendoc(source)
        tidychef_selectables = []

        for worksheet in spreadsheet.sheets:

            table = Table()
            for y, row in enumerate(worksheet.rows()):
                for x, cell in enumerate(row):
                    table.add_cell(
                        Cell(
                            x=int(x),
                            y=int(y),
                            value=str(cell.plaintext())
                            if cell.value is not None
                            else "",
                        )
                    )

            tidychef_selectables.append(
                selectable(table, source=source, name=worksheet.name)
            )
        return tidychef_selectables
