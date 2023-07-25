"""
Source code for the acquirer class that power the data acquisition methods.

You would not typically be calling this directly outside of advanced users
utilising kwargs for unanticipated and/or niche uses cases.

In the vast majority of circumstances it is both easier and more reliable
to use the provided wrappers.

acquire.csv.local()
acquire.csv.remote()
etc...
"""
import re
from typing import Any, Callable, List, Optional, Union

from tidychef.acquire.base import BaseReader
from tidychef.exceptions import ZeroAcquiredTablesError
from tidychef.selection.selectable import Selectable


def acquirer(
    source: Any,
    reader: BaseReader,
    selectable: Selectable,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    **kwargs,
) -> Union[List[Selectable], Selectable]:
    """
    The principle data acquisition function. Wraps the reader
    to enable pre and post hook.

    :param source: A source appropriate for the provided BaseReader
    :param reader: A class that implements tidychef.acquire.base.BaseReader
    :param selectable: A class that implements tidychef.selection.selectable.Selectable
    :param pre_hook: A callable that can take source as an argument
    :param post_hook: A callable that can take the output of reader.parse() as an argument.
    :return: A single or list of class Selectable or inheritor of as returned by reader after
    optional modification by post_hook.
    """

    # Execute pre load hook
    if pre_hook:
        source = pre_hook(source)

    parsed = reader.parse(source, selectable, **kwargs)

    if reader.tables:
        assert isinstance(
            parsed, list
        ), "You can only use tables= where acquire is returning a list of selectabes."
        initial_table_names = [x.name for x in parsed]
        parsed = [x for x in parsed if re.match(reader.tables, x.name)]
        if len(parsed) == 1:
            parsed = parsed[0]
        if isinstance(parsed, list):
            if len(parsed) == 0:
                raise ZeroAcquiredTablesError(
                    f"""
                    The tables regex you provided: {reader.tables}
                    Has resulted in no tables being acquired.

                    The table names in question were:
                    {initial_table_names}
                    """
                )

    # Execute post load hook
    if post_hook:
        parsed = post_hook(parsed)

    return parsed
