from pathlib import Path
from typing import Union
from datachef.models.source.input import BaseInput
from datachef import acquire
from datachef.exceptions import FileInputError
from datachef.acquire.base import BaseReader
from datachef.selection.selectable import Selectable
from tests.fixtures import path_to_fixture
import pytest

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
        csv_path,
        reader=FakeReader,
        selectable=Selectable
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
    acquire.csv.local(csv_path, pre_hook=lambda x: Path(str(x.resolve())+".csv"))
