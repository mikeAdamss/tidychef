from pathlib import Path

import datachef.constants
from datachef.exceptions import UnsupportedLocalFileError


def identify_local_input_type(input_path: Path) -> str:
    """
    Where provided a pathlib.Path object. Determine the file type
    from the extension.
    """

    assert isinstance(input_path, Path)

    if str(input_path.absolute()).endswith(
        datachef.constants.SUPPORTED_LOCAL_FILETYPES.CSV
    ):
        return datachef.constants.SUPPORTED_LOCAL_FILETYPES.CSV
    else:
        raise UnsupportedLocalFileError(
            f"Cannot identify local file type, expecting one of: {datachef.constants.SUPPORTED_LOCAL_FILETYPES}"
        )
