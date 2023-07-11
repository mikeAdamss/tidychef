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
from typing import Any, Callable, List, Optional, Union

from datachef.acquire.base import BaseReader
from datachef.selection.selectable import Selectable


def acquirer(
    source: Any,
    reader: Optional[BaseReader] = None,
    selectable: Optional[Selectable] = None,
    pre_hook: Optional[Callable] = None,
    post_hook: Optional[Callable] = None,
    **kwargs
) -> Union[List[Selectable], Selectable]:
    """
    :param path: The path of the file to wrap
    :type path: str
    :param field_storage: The :class:`FileStorage` instance to wrap
    :type field_storage: FileStorage
    :param temporary: Whether or not to delete the file when the File
    instance is destructed
    :type temporary: bool
    :returns: A buffered writable file descriptor
    :rtype: BufferedFileStorage
    """

    # Execute pre load hook
    if pre_hook:
        source = pre_hook(source)

    parsed = reader.parse(source, selectable=selectable, **kwargs)

    # Execute post load hook
    if post_hook:
        parsed = post_hook(parsed)

    return parsed
