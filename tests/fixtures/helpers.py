from pathlib import Path

# TODO - necessary?

# Fixture dir shorthand
allowed_fixtures_locations = ["csv", "preview", "json/closest", "xls", "xlsx"]
fixture_locations_as_str = ",".join(allowed_fixtures_locations)

fixture_dir = Path(__file__).parent


def path_to_fixture(subdir: str, file_wanted: str, assert_exists=True) -> Path:
    """
    Given the fixture subdir and the filename, get the path to a fixture
    """

    assert (
        subdir in allowed_fixtures_locations
    ), f"Fixtures can be taken from the sub directories: {fixture_locations_as_str}"

    fixture_path = Path(fixture_dir / subdir / file_wanted)
    if assert_exists:
        assert (
            fixture_path.exists()
        ), f"The fixture {fixture_path.absolute()} does not exist"

    return fixture_path
