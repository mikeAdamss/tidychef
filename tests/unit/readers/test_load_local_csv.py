from pathlib import Path

from pivoter.models.source.input import BaseInput
from pivoter.readers import reader
from tests.fixtures import path_to_fixture


def test_read_local_csv_from_path():
    """
    Test local file loader for csv from path
    """
    csv_path: Path = path_to_fixture("csv", "simple.csv")
    sheet: BaseInput = reader.read_local(csv_path)

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 2600  # A-Z for 100 rows


def test_read_local_csv_from_str():
    """
    Test local file loader for csv from str
    """
    csv_path: Path = path_to_fixture("csv", "simple.csv")
    sheet: BaseInput = reader.read_local(str(csv_path.absolute()))

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 2600  # A-Z for 100 rows
