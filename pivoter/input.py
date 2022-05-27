"""
The mechanism for getting inputs into pivoter
"""

from pathlib import Path
from typing import Union

import pivoter.utils.fileutils
import pivoter.models.source
import pivoter.handlers.input
import pivoter.constants

def read_file(input: Union[str, Path]) -> pivoter.models.source.Input:
    """
    Simplest input, read from a local file.
    """

    input_path: Path = pivoter.utils.fileutils.ensure_existing_path(input)
    file_type: str = pivoter.utils.fileutils.identify_local_input_type(input)

    if file_type == pivoter.constants.SUPPORTED_LOCAL_FILETYPES.CSV:
        handler = pivoter.handlers.input.LocalCsvHandler

    instantiated_handler: pivoter.handlers.input.BaseInputHandler = handler(input_path)
    input_parsed: pivoter.models.source.Input = instantiated_handler.parse()

    return input_parsed