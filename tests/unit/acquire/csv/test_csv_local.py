from pathlib import Path

from tests.fixtures import path_to_fixture
from tidychef import acquire
from tidychef.selection.selectable import Selectable


def test_acquire_local_csv():
    """
    Test that the acquire fuction works with a local csv
    """

    csv_path = path_to_fixture("csv", "simple-small.csv")
    assert isinstance(acquire.csv.local(csv_path), Selectable)

    csv_path_as_str = csv_path.resolve()
    assert isinstance(acquire.csv.local(csv_path_as_str), Selectable)


def test_read_local_csv_from_path():
    """
    Test local file loader for csv from path
    """
    csv_path: Path = path_to_fixture("csv", "simple.csv")
    sheet: Selectable = acquire.csv.local(csv_path)

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 2600  # A-Z for 100 rows


def test_read_local_csv_from_str():
    """
    Test local file loader for csv from str
    """
    csv_path: Path = path_to_fixture("csv", "simple.csv")
    sheet: Selectable = acquire.csv.local(str(csv_path.absolute()))

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 2600  # A-Z for 100 rows
