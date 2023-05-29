"""
Acquire is the principle gateway for acquiring new source data
making http gets where necessary before passing the source into the readers.
"""

from typing import Any, Optional, Union

from datachef.readers.base import BaseReader
from datachef.readers.objects.list import ListReader
from datachef.readers.reader import read_local
from datachef.selection.selectable import Selectable


def acquire(
    source: Any,
    reader: Optional[BaseReader] = None,
    selectable: Selectable = None,
) -> Selectable:
    """
    Principle function for getting new data sources into datachef.

    Where no keyword arguments are provided acquire will attempt
    to use the appropriate reader (thing to read the source data
    format) and selectable (thing that provides your cell selection
    methods) where passed a file, url or python object as
    the positional argument.

    To provided more nuanced control for advanced users and to
    provide a point of intervention for custom behaviours, users
    can do so via following inheritance kwargs:

    :reader:      Anything that implements datachef.readers.base: BaseReader.
    :selectable:  Anything that is a child class of datachef.selection.selectable:Selectable

    For supported python objects, see:
    datachef.readers.objects.*
    """

    # TODO: check if source it a python object and call
    # the appropriate handler
    if isinstance(source, list):
        return ListReader(source).parse()

    # If it's not a python type, then it's either a
    # local or remote source file

    # TODO: check if source if a url
    # then write read_remote

    return read_local(source, override_reader=reader, override_selectable=selectable)
