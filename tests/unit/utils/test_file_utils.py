from pathlib import Path

import pytest

from datachef.exceptions import FileInputError
from datachef.utils import fileutils
from tests.fixtures import path_to_fixture


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
