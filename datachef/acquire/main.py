"""
Source code for the acquirer class that power the data acquisition methods.

You would not typically be calling this directly outside of advanced users
utilising kwargs for unanticipated and/or niche uses cases.

In the vast majority of cirumstances it is both easier and more reliable
to use the provided wrappers.

acquire.csv.local()
acquire.csv.remote()
etc...
"""
from typing import Any, Callable, Optional

from datachef.acquire.base import BaseReader
from datachef.selection.selectable import Selectable


def acquirer(
    source: Any,
    reader: Optional[BaseReader] = None,
    selectable: Optional[Selectable] = None,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    **kwargs
) -> Selectable:
    """
    The basic acquiring function that all of the other
    acquire functions call.

    You would not typically be calling this directly
    outside of advanced users utilising kwargs for
    unanticipated and/or niche uses cases.
    """

    # Execute pre load hook
    if pre_hook:
        source = pre_hook(source)

    parsed = reader.parse(source, selectable=selectable, **kwargs)

    # Execute post load hook
    if post_hook:
        parsed = post_hook(parsed)

    return parsed
