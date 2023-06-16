from pathlib import Path

from datachef.models.source.input import BaseInput
from datachef.acquire.acquirer import acquirer
from datachef.acquire.base import BaseReader
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
    str_instead_of_selectable = acquirer(
        csv_path,
        reader=FakeReader,
        selectable=Selectable
    )
    assert str_instead_of_selectable == "foo"