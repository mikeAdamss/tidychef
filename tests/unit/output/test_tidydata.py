from pathlib import Path

import pytest

from datachef.cardinal.directions import above, left
from datachef.column import Column
from datachef.lookup import Constant, Directly
from datachef.output.tidydata import TidyData
from datachef.selection import filters
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_wide_band_tab
from tests.fixtures.helpers import path_to_fixture
from tests.unit.helpers import assert_csvs_match



@pytest.fixture
def tidy() -> TidyData:
    """
    A relatively simple definition of a populated TidyData class.
    """
    selectable_wide_band_tab: Selectable = fixture_wide_band_tab()

    observations = selectable_wide_band_tab.excel_ref("B4:K6").filter(
        filters.is_numeric
    )
    assets = selectable_wide_band_tab.excel_ref("2").is_not_blank()
    member = (
        selectable_wide_band_tab.excel_ref("4:7")
        .is_not_blank()
        .filter(filters.is_not_numeric)
    )

    tidy = TidyData(
        observations,
        [
            Column("Genre", Constant("Rock & Roll")),
            Column("Assets", Directly(assets, above)),
            Column("Member", Directly(member, left)),
        ],
    )

    return tidy


def test_tidydata_can_be_transformed(tidy: TidyData):
    """
    Test that calling _transform() result in a populated
    ._data attribute.
    """
    assert tidy._data is None
    tidy._transform()
    assert tidy._data is not None

def test_tidydata_internal_representation_is_as_expected(tidy: TidyData):
    """
    Test that the ._data attribute of TidyData contains the expected
    data once _transform() has been called.
    """

    tidy._transform()
    expected_data = [
        ["Value", "Genre", "Assets", "Member"],
        ["1", "Rock & Roll", "Houses", "John"],
        ["5", "Rock & Roll", "Cars", "John"],
        ["9", "Rock & Roll", "Boats", "John"],
        ["2", "Rock & Roll", "Houses", "Keith"],
        ["6", "Rock & Roll", "Cars", "Keith"],
        ["10", "Rock & Roll", "Boats", "Keith"],
        ["2", "Rock & Roll", "Houses", "Paul"],
        ["6", "Rock & Roll", "Cars", "Paul"],
        ["10", "Rock & Roll", "Boats", "Paul"],
        ["3", "Rock & Roll", "Houses", "Mick"],
        ["7", "Rock & Roll", "Cars", "Mick"],
        ["11", "Rock & Roll", "Boats", "Mick"],
        ["2", "Rock & Roll", "Houses", "George"],
        ["7", "Rock & Roll", "Cars", "George"],
        ["11", "Rock & Roll", "Boats", "George"],
        ["3", "Rock & Roll", "Houses", "Charlie"],
        ["8", "Rock & Roll", "Cars", "Charlie"],
        ["12", "Rock & Roll", "Boats", "Charlie"],
    ]
    assert tidy._data == expected_data

def test_tidydata_can_be_written_to_csv(tidy: TidyData):
    """
    Tests that a TidyData objects can be written to a
    csv file via the to_csb method.
    """

    here = Path(__file__).parent
    test_csv_output_path = Path(here / "temporary.csv")
    tidy.to_csv(test_csv_output_path)

    correct_csv_fixture_path: Path = path_to_fixture("csv", "test_output.csv")

    assert_csvs_match(test_csv_output_path, correct_csv_fixture_path)
