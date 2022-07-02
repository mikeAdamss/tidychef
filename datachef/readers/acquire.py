"""
Acquire is the principle gateway for acquiring new source data
making http gets where necessary before passing the source into the readers.
"""

from typing import Any, Optional

from datachef.readers.base import BaseReader
from datachef.readers.objects.list import ListReader
from datachef.readers.reader import read_local
from datachef.selection.selectable import Selectable


def acquire(
    source: Any,
    override_reader: Optional[BaseReader] = None,
    override_selectable: Selectable = None,
) -> Selectable:
    """
    Principle method for getting new data sources into datachef.
    """

    # TODO: check if source it a python object and call
    # the appropriate handler
    if isinstance(source, list):
        return ListReader(source).parse()

    # If it's not a python type, then it's either a
    # local or remote source file

    # TODO: check if source if a url
    # then write read_remote

    return read_local(
        source, override_reader=override_reader, override_selectable=override_selectable
    )
