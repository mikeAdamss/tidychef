from pathlib import Path

import pivoter.constants
import pivoter.exceptions.common


def identify_local_input_type(input_path: Path) -> str:
    """
    Where provided a pathlib.Path object. Determine the file type
    from the extension.
    """

    if str(input_path.absolute()).endswith(
        pivoter.constants.SUPPORTED_LOCAL_FILETYPES.CSV
    ):
        return pivoter.constants.SUPPORTED_LOCAL_FILETYPES.CSV
    else:
        raise pivoter.exceptions.common.UnsupportedLocalFileError(
            f"Cannot identify local file type, expecting one of: {pivoter.constants.SUPPORTED_LOCAL_FILETYPES}"
        )
