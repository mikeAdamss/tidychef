from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest

from tests.fixtures import path_to_fixture
from tidychef import acquire
from tidychef.acquire.base import BaseReader
from tidychef.acquire.main import acquirer
from tidychef.exceptions import FileInputError, ZeroAcquiredTablesError
from tidychef.selection.selectable import Selectable


def test_reader_can_be_overwritten():
    """
    Test that the base reader can check source and
    raise if not class:Path.
    """

    class FakeReader(BaseReader):
        def parse(self, *args, **kwargs):
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

    def table_name_adding_hook(selection: Selectable):
        selection._name = "foo"
        return selection

    table: Selectable = acquire.csv.local(csv_path, post_hook=table_name_adding_hook)
    assert table.name == "foo"


def test_tables_regex():
    """
    Test the acquirer filter by tables logic works as expected.
    """

    csv_path: Path = path_to_fixture("csv", "simple.csv", assert_exists=False)

    @dataclass
    class FakeTable:
        name: str

    class FakeReader(BaseReader):
        def parse(self, *args, **kwargs):
            return [FakeTable("foo"), FakeTable("bar"), FakeTable("baz")]

    tables: List[FakeTable] = acquirer(
        csv_path, reader=FakeReader("^b.*$"), selectable=Selectable
    )
    table_names = [x.name for x in tables]
    assert "bar" in table_names
    assert "baz" in table_names

    # Test we de-listified where we've filtered down to 1 table
    table: FakeTable = acquirer(
        csv_path, reader=FakeReader("^f.*$"), selectable=Selectable
    )
    assert isinstance(table, FakeTable)

    with pytest.raises(ZeroAcquiredTablesError):
        acquirer(csv_path, reader=FakeReader("aksjdkasldklakl"), selectable=Selectable)
