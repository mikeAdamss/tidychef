import pytest

from datachef.exceptions import FileInputError
from datachef.readers.base import BaseReader


def test_base_reader_can_raise_for_no_path_parameter():
    """
    Test that the base reader can check source and
    raise if not class:Path.
    """

    class FakeReader(BaseReader):
        def parse():
            """never called"""

    not_a_path = "foo"
    reader = FakeReader(not_a_path)

    with pytest.raises(FileInputError):
        reader._raise_if_source_is_not_path()
