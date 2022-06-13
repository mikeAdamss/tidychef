"""
Wrappers and utilities bringing together the functionality within
./readers for convenience.
"""

from pathlib import Path
from typing import Union

from pivoter.utils import fileutils
import pivoter.models.source
from pivoter.readers import LocalCsvReader, BaseReader
from pivoter.constants import SUPPORTED_LOCAL_FILETYPES


def read_local_file(input: Union[str, Path]) -> pivoter.models.source.Input:
    """
    Simplest input, read from a local file.
    """

    input_path: Path = fileutils.ensure_existing_path(input)
    file_type: str = fileutils.identify_local_input_type(input_path)

    # note: else raise is not required as unsupported file types is
    # handled by identify_local_input_type
    if file_type == SUPPORTED_LOCAL_FILETYPES.CSV:
        handler_insantiated: BaseReader = LocalCsvReader(input_path)

    return handler_insantiated.parse()
