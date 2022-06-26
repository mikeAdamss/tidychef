from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from datachef.models.source.cell import BaseCell, Cell
from datachef.models.source.table import LiveTable, Table
from datachef.selection.base import Selectable

# Fixture dir shorthand
CSV = "csv"
PREVIEW = "preview"
fixtures_locations = [CSV, PREVIEW]
fixture_locations_as_str = ",".join(fixtures_locations)

fixture_dir = Path(__file__).parent


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
