from pathlib import Path

import pytest

from datachef import acquire
from datachef.acquire.base import BaseReader
from datachef.exceptions import FileInputError, UnnamedTableError
from datachef.selection.selectable import Selectable
from tests.fixtures import path_to_fixture


def test_reader_can_be_overwritten():
    """
    Test that the base reader can check source and
    raise if not class:Path.
    """

    class FakeReader(BaseReader):
        def parse(self, **kwargs):
            return "foo"

    csv_path: Path = path_to_fixture("csv", "simple.csv")
    str_instead_of_selectable = acquire.acquirer(
        csv_path, reader=FakeReader, selectable=Selectable
    )
    assert str_instead_of_selectable == "foo"


def test_pre_hook():
    """
    Test the pre hook callable works as intended
    """

    # Path but missing the csv file extension
    csv_path: Path = path_to_fixture("csv", "simple", assert_exists=False)

    with pytest.raises(FileInputError):
        acquire.csv.local(csv_path)

    # Now it works
    acquire.csv.local(csv_path, pre_hook=lambda x: Path(str(x.resolve()) + ".csv"))


def test_post_hook():
    """
    Test the post hook callable works as intended
    """

    csv_path: Path = path_to_fixture("csv", "simple.csv", assert_exists=False)

    # Originally has no table so raises
    with pytest.raises(UnnamedTableError):
        table: Selectable = acquire.csv.local(csv_path)
        assert table.name == "foo"

    def table_name_adding_hook(selection: Selectable):
        selection._name = "foo"
        return selection

    table: Selectable = acquire.csv.local(csv_path, post_hook=table_name_adding_hook)
    assert table.name == "foo"
