"""
Wrappers and utilities bringing together the functionality within
./readers for convenience.
"""

from pathlib import Path
from typing import Optional, Union

from datachef.constants.files import SUPPORTED_LOCAL_FILETYPES
from datachef.acquire.base import BaseReader
from datachef.acquire.csv.local import LocalCsvReader
from datachef.selection.selectable import Selectable
from datachef.utils import fileutils


def read_local(
    path_or_str: Union[str, Path],
    override_reader: Optional[BaseReader] = None,
    override_selectable: Optional[Selectable] = None,
) -> Selectable:
    """
    Reads an input from a local file.

    The reader to be used will be derived from the input, or
    can be passed in via override_reader.

    The Selectable class returned can be overwritten using
    override_selectable. This is to given an advacned user
    some control over the palette of selection methods made
    availible for a given source.
    """

    input_path: Path = fileutils.ensure_existing_path(path_or_str)
    file_type: str = fileutils.identify_local_input_type(input_path)

    if override_reader:
        handler_insantiated: BaseReader = override_reader(input_path)
    else:
        if file_type == SUPPORTED_LOCAL_FILETYPES.CSV:
            handler_insantiated: BaseReader = LocalCsvReader(input_path)

    if override_selectable:
        return handler_insantiated.parse(selectable=override_selectable)
    return handler_insantiated.parse()
