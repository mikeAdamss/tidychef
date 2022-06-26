from pathlib import Path
from typing import Union, Optional
from datachef.selection.base import Selectable
from datachef.readers.base import BaseReader
from datachef.readers.reader import read_local

def acquire(source: Union[str, Path],
    override_reader: Optional[BaseReader] = None,
    override_selectable: Selectable = None) -> Selectable:
    """
    Wrapper for the reader functions.
    """

    # TODO: check if source if a url
    # then write read_remote

    return read_local(source, override_reader=override_reader, override_selectable=override_selectable)
