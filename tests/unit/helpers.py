from pathlib import Path
from typing import List, Optional

from pivoter.models.source.cell import Cell
from pivoter.models.source.table import Table, LiveTable
from pivoter.selection.base import Selectable

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


def single_table_test_input(
    cells: List[Cell],
    table_name: Optional[str] = None,
    input_type: Selectable = Selectable,
) -> Selectable:
    """
    Returns a subclass of class:Input consisting of a single table
    comprised of the provided class:Cell objects.

    The sub class of Input (and mixin methods availible) are
    defined by input_type
    """
    return input_type(
        is_singleton_table=True,
        selected_table=LiveTable.from_table(Table(cells), name=table_name),
        had_initial_path=None,
        tables=None,
    )


def multiple_table_test_input(
    tables: List, input_type: Selectable = Selectable
) -> Selectable:
    """
    Returns a subclass of  class:Input consisting of a single table
    comprised of the provided class:Cell objects

    The sub class of Input (and mixin methods availible) are
    defined by input_type

    Tables is a list of inputs in the form: [§§§
        [List[Cell], Optional[<table name>]],
        [List[Cell], Optional[<table name>]]
    ]
    """
    all_tables = []
    for table in tables:
        all_tables.append(LiveTable.from_table(Table(table[0]), name=table[1]))

    return input_type(
        is_singleton_table=False,
        selected_table=all_tables[0],
        had_initial_path=None,
        tables=all_tables,
    )
