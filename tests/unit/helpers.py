from pathlib import Path
from typing import List

from pivoter.models.source import Cell, Table, Input, LiveTable

# Fixture dir shorthand
CSV = "csv"
fixtures_locations = [CSV]
fixture_locations_as_str = ",".join(fixtures_locations)

pivoter_dir = Path(__file__).parent.parent.parent
fixture_dir = Path(pivoter_dir / "tests" / "fixtures")


def path_to_fixture(subdir: str, file_wanted: str) -> Path:
    """
    Given the fixture subdir and the filename, get the path to a fixture
    """

    assert (
        subdir in fixtures_locations
    ), f"Fixtures can be taken from the sub directories: {fixture_locations_as_str}"

    fixture_path = Path(fixture_dir / subdir / file_wanted)
    assert (
        fixture_path.exists()
    ), f"The fixture {fixture_path.absolute()} does not exist"

    return fixture_path


def single_table_input(name: str, cells: List[Cell]) -> Input:
    return Input(
        is_singelton_table=True,
        selected_table=LiveTable.from_table(name, Table(cells)),
        had_initial_path=None,
        tables=None,
    )