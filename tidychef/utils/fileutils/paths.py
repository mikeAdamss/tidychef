from pathlib import Path
from typing import Union

from tidychef.exceptions import FileInputError


def ensure_existing_path(maybe_path: Union[Path, str]) -> Path:
    """
    When given a Path or str representing an existing path, ensure that:

    a.) it is a Path (convert where necessary)
    b.) confirm it exists
    """

    if not isinstance(maybe_path, (Path, str)):
        raise FileInputError(
            "To use a direct file input, you must provide a pathlib.Path object or a str representing one"
        )

    if isinstance(maybe_path, str):
        maybe_path = Path(maybe_path)

    if not maybe_path.exists():
        raise FileInputError(
            f"A file at the path {maybe_path.absolute()} does not exist."
        )

    assert isinstance(maybe_path, Path)

    return maybe_path
