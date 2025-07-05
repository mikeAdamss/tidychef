"""
Holds the code that defines the local xlsx reader.
"""

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, List, Optional, Union

import ezodf
import requests
import validators
from ezodf.document import PackagedDocument

from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.ods.ods import OdsSelectable
from tidychef.selection.selectable import Selectable
from tidychef.utils.http.caching import get_cached_session


def http(
    source: Union[str, Path],
    selectable: Selectable = OdsSelectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    session: requests.Session = None,
    cache: bool = True,
    tables: str = None,
    **kwargs,
) -> Union[OdsSelectable, List[OdsSelectable]]:
    """
    Read data from a Path (or string representing a path)
    present on the same machine where tidychef is running.

    :param source: A url.
    :param selectable: A class that implements tidychef.selection.selectable.Selectable of an inheritor of. Default is OdsSelectable.
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of HttpOdsReader.parse() as an argument.
    :param session: An optional requests.Session object.
    :param cache: Boolean flag for whether or not to cache get requests.
    :return: A single populated Selectable of type as specified by selectable param.
    """

    assert validators.url(source), f"'{source}' is not a valid http/https url."

    return acquirer(
        source,
        HttpOdsReader(tables),
        selectable,
        pre_hook=pre_hook,
        post_hook=post_hook,
        session=session,
        cache=cache,
        **kwargs,
    )


class HttpOdsReader(BaseReader):
    """
    A reader to lead in a source where that source is a locally
    held xlsx file.
    """

    def parse(
        self,
        source: str,
        selectable: Selectable = OdsSelectable,
        session: requests.Session = None,
        cache: bool = True,
        **kwargs,
    ) -> List[OdsSelectable]:
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

        # TODO: faster!
        # So ezodf doesn't want to take a fileobject but instead needs a
        # solid file. For now we're writing to a temp (self deleting) file
        # and passing it in.
        # This works but there's whole file write and re-read more in here
        # that their needs to be.

        temp_file = NamedTemporaryFile()
        temp_file.write(response.content)
        temp_file.seek(0)

        spreadsheet: PackagedDocument = ezodf.opendoc(temp_file.name)
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

        temp_file.close()
        return tidychef_selectables
