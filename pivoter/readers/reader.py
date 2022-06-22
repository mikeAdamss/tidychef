"""
Wrappers and utilities bringing together the functionality within
./readers for convenience.
"""

from pathlib import Path
from typing import Optional, Union

from pivoter.utils import fileutils
from pivoter.readers import LocalCsvReader, BaseReader
from pivoter.constants import SUPPORTED_LOCAL_FILETYPES
from pivoter.selection.base import Selectable


def read_local(
    path_or_str: Union[str, Path],
    override_reader: Optional[BaseReader] = None,
    override_selectable: Selectable = None,
) -> Selectable:
    """
    Reads an input from a local file.

    The reader to be used will be derived from the input, or
    can be passed in via override_reader.

    The Selectable class returned can be overwritten using
    override_selectable. This is to enable source file
    specific methods (such as .excel_ref()) that don't necessarily
    make sense as standard with all input types (such as csv).

    The above functionality is provided as best effort for edge
    cases and will not be supported or even possible in all instances.
    """

    input_path: Path = fileutils.ensure_existing_path(path_or_str)
    file_type: str = fileutils.identify_local_input_type(input_path)

    if override_reader:
        handler_insantiated: BaseReader = override_reader(input_path)
    else:
        if file_type == SUPPORTED_LOCAL_FILETYPES.CSV:
            handler_insantiated: BaseReader = LocalCsvReader(
                input_path
            )

    if override_selectable:
        return handler_insantiated.parse(selectable=override_selectable)
    else:
        return handler_insantiated.parse()
