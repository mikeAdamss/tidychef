from pathlib import Path

fixture_dir = Path(__file__).parent


def path_to_fixture(subdir: str, file_wanted: str, assert_exists=True) -> Path:
    """
    Given the fixture subdir and the filename, get the path to a fixture
    """

    fixture_path = Path(fixture_dir / subdir / file_wanted)
    if assert_exists:
        assert (
            fixture_path.exists()
        ), f"The fixture {fixture_path.absolute()} does not exist"

    return fixture_path
