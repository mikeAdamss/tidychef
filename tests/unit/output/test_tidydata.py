import pytest

from datachef.cardinal.directions import above, left
from datachef.column import Column
from datachef.lookup import Constant, Directly
from datachef.output.tidydata import TidyData
from datachef.selection import filters
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_wide_band_tab


@pytest.fixture
def selectable_wide_band_tab():
    return fixture_wide_band_tab()


def test_tidydata_constructor_and_ouput(selectable_wide_band_tab: Selectable):
    """
    Test tidy constructor works as expected with
    a simple use case.
    """

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

    assert tidy.data is None
    tidy.transform()
    assert tidy.data is not None

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
    assert tidy.data == expected_data
