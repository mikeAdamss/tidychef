from pathlib import Path

import pytest

from datachef.constants import SUPPORTED_LOCAL_FILETYPES
from datachef.exceptions import FileInputError, UnsupportedLocalFileError
from datachef.utils import fileutils
from tests.fixtures import path_to_fixture


def test_identify_local_input_type_with_known_input_type():
    """
    Test we can successfuly identify known local input types
    from their file extensions.
    """

    for known_filetype in SUPPORTED_LOCAL_FILETYPES.__dict__.values():
        filepath_to_nothing: Path = Path(f"I-dont-exist.{known_filetype}")
        input_type = fileutils.identify_local_input_type(filepath_to_nothing)
        assert (
            input_type == known_filetype
        ), f"failing to identify registered file type of {input_type} from {filepath_to_nothing}"


def test_identify_local_input_type_with_unknown_input_type():
    """
    Test an error is raised when an unknown local input type
    is provided.
    """

    filepath_to_nothing: Path = Path("I-dont-exist.wonderfulfileextension")
    with pytest.raises(UnsupportedLocalFileError):
        fileutils.identify_local_input_type(filepath_to_nothing)


def test_ensure_existing_path_from_str_where_exists():
    """
    Where a str is provided that correctly points to a file, confirm
    it is correctly converted to a Path object.
    """

    arbitrary_existing_file = path_to_fixture("csv", "simple.csv")
    arbitrary_existing_file_str = str(arbitrary_existing_file.resolve())
    p = fileutils.ensure_existing_path(arbitrary_existing_file_str)
    assert isinstance(p, Path)


def test_ensure_existing_path_raises_for_not_existing():
    """
    Where a path to a non existing Path is provided, make sure
    the appropriate error is raised.
    """

    filepath_to_nothing: Path = Path("I-dont-exist.wonderfulfileextension")
    with pytest.raises(FileInputError):
        fileutils.ensure_existing_path(filepath_to_nothing)


def test_ensure_existing_path_unexpected_type_raised_err():
    """
    Where we path an unexpected type into fileutils.ensure_existing_path,
    confirm the expected error is raised.
    """

    neither_path_nor_str = None
    with pytest.raises(FileInputError):
        fileutils.ensure_existing_path(neither_path_nor_str)
