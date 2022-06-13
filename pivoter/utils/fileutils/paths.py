from pathlib import Path
from typing import Union

from pivoter.exceptions import FileInputError


def ensure_existing_path(maybe_path: Union[Path, str]) -> Path:
    """
    When given something that is expected to be a existing path, ensure that:

    a.) it is
    b.) it exists
    """

    if not isinstance(maybe_path, (Path, str)):
        raise FileInputError(
            "To use a direct file input, you must provide a pathlib.Path objdct or a str representing one"
        )

    if isinstance(maybe_path, str):
        maybe_path = Path(maybe_path)

    if not maybe_path.exists():
        raise FileInputError(
            f"A file at the path {maybe_path.absolute()} does not exist."
        )

    assert isinstance(maybe_path, Path)

    return maybe_path
