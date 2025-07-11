import copy
import json
import os
import uuid
from pathlib import Path

import pytest

from tests.fixtures import fixture_wide_band_tab
from tests.fixtures.helpers import path_to_fixture
from tests.unit.helpers import assert_csvs_match
from tidychef.column import Column
from tidychef.direction.directions import above, below, left, right
from tidychef.exceptions import DroppingNonColumnError, MisalignedHeadersError
from tidychef.lookup.engines.constant import Constant
from tidychef.lookup.engines.direct import Directly
from tidychef.output.tidydata import TidyData
from tidychef.selection import filters
from tidychef.selection.selectable import Selectable


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
        observations.label_as("Value"),
        Column(Constant("Genre", "Rock & Roll")),
        Column(Directly("Assets", assets, above)),
        Column(Directly("Member", member, left)),
    )

    return tidy


@pytest.fixture
def tidy_with_obs_apply() -> TidyData:
    """
    A relatively simple definition of a populated TidyData class
    with an apply used.
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
        observations.label_as("Value"),
        Column(Constant("Genre", "Rock & Roll")),
        Column(Directly("Assets", assets, above)),
        Column(Directly("Member", member, left)),
        obs_apply=lambda x: "foo " + x,
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
    assert tidy._data_as_table_of_strings() == expected_data
    assert len(tidy) == 19


def test_tidydata_internal_representation_is_as_expected_with_apply(
    tidy_with_obs_apply: TidyData,
):
    """
    Test that the ._data attribute of TidyData contains the expected
    data once _transform() has been called.
    """

    tidy_with_obs_apply._transform()
    expected_data = [
        ["Value", "Genre", "Assets", "Member"],
        ["foo 1", "Rock & Roll", "Houses", "John"],
        ["foo 5", "Rock & Roll", "Cars", "John"],
        ["foo 9", "Rock & Roll", "Boats", "John"],
        ["foo 2", "Rock & Roll", "Houses", "Keith"],
        ["foo 6", "Rock & Roll", "Cars", "Keith"],
        ["foo 10", "Rock & Roll", "Boats", "Keith"],
        ["foo 2", "Rock & Roll", "Houses", "Paul"],
        ["foo 6", "Rock & Roll", "Cars", "Paul"],
        ["foo 10", "Rock & Roll", "Boats", "Paul"],
        ["foo 3", "Rock & Roll", "Houses", "Mick"],
        ["foo 7", "Rock & Roll", "Cars", "Mick"],
        ["foo 11", "Rock & Roll", "Boats", "Mick"],
        ["foo 2", "Rock & Roll", "Houses", "George"],
        ["foo 7", "Rock & Roll", "Cars", "George"],
        ["foo 11", "Rock & Roll", "Boats", "George"],
        ["foo 3", "Rock & Roll", "Houses", "Charlie"],
        ["foo 8", "Rock & Roll", "Cars", "Charlie"],
        ["foo 12", "Rock & Roll", "Boats", "Charlie"],
    ]
    assert tidy_with_obs_apply._data_as_table_of_strings() == expected_data
    assert len(tidy_with_obs_apply) == 19


def test_tidydata_internal_representation_with_dropped_column_is_as_expected(
    tidy: TidyData,
):
    """
    Test that the ._data attribute of TidyData contains the expected
    data once _transform() has been called when we drop a column.
    """

    tidy.drop = ["Assets"]
    tidy._transform()
    expected_data = [
        ["Value", "Genre", "Member"],
        ["1", "Rock & Roll", "John"],
        ["5", "Rock & Roll", "John"],
        ["9", "Rock & Roll", "John"],
        ["2", "Rock & Roll", "Keith"],
        ["6", "Rock & Roll", "Keith"],
        ["10", "Rock & Roll", "Keith"],
        ["2", "Rock & Roll", "Paul"],
        ["6", "Rock & Roll", "Paul"],
        ["10", "Rock & Roll", "Paul"],
        ["3", "Rock & Roll", "Mick"],
        ["7", "Rock & Roll", "Mick"],
        ["11", "Rock & Roll", "Mick"],
        ["2", "Rock & Roll", "George"],
        ["7", "Rock & Roll", "George"],
        ["11", "Rock & Roll", "George"],
        ["3", "Rock & Roll", "Charlie"],
        ["8", "Rock & Roll", "Charlie"],
        ["12", "Rock & Roll", "Charlie"],
    ]
    assert tidy._data_as_table_of_strings() == expected_data
    assert len(tidy) == 19


def test_tidydata_internal_representation_with_dropped_column_is_as_expected(
    tidy: TidyData,
):
    """
    Test that the ._data attribute of TidyData contains the expected
    data once _transform() has been called when we drop the original
    observation column
    """

    tidy.drop = ["Value", "Assets"]
    tidy._transform()
    expected_data = [
        ["Genre", "Member"],
        ["Rock & Roll", "John"],
        ["Rock & Roll", "John"],
        ["Rock & Roll", "John"],
        ["Rock & Roll", "Keith"],
        ["Rock & Roll", "Keith"],
        ["Rock & Roll", "Keith"],
        ["Rock & Roll", "Paul"],
        ["Rock & Roll", "Paul"],
        ["Rock & Roll", "Paul"],
        ["Rock & Roll", "Mick"],
        ["Rock & Roll", "Mick"],
        ["Rock & Roll", "Mick"],
        ["Rock & Roll", "George"],
        ["Rock & Roll", "George"],
        ["Rock & Roll", "George"],
        ["Rock & Roll", "Charlie"],
        ["Rock & Roll", "Charlie"],
        ["Rock & Roll", "Charlie"],
    ]
    assert tidy._data_as_table_of_strings() == expected_data
    assert len(tidy) == 19


def test_tidydata_drop_raises_expected_error_for_non_existent_column(tidy: TidyData):
    """
    Confirm the expected error is raised where we are trying to drop
    a column that does not exist in the data.
    """

    tidy.drop = ["foo"]

    with pytest.raises(DroppingNonColumnError):
        tidy._transform()


def test_tidydata_from_many(tidy: TidyData):
    """
    Test that the TidyData.from_many() static method works
    as expected.
    """
    assert len(tidy) == 19

    big_tidy = TidyData.from_tidy(tidy, tidy)

    # double, minus 1 as we dont need two copies of the
    # header row.
    assert len(big_tidy) == 37


def test_tidydata_from_many_misaligned_headers(tidy: TidyData):
    """
    Test that the TidyData.from_many() static method raises an
    appropriate error where tables with different header
    columns are used.
    """

    # Alter the Value column to Value2 in tidy2
    tidy2 = copy.deepcopy(tidy)
    tidy2._transform()
    tidy2._data[0] = ["Value2", "Genre", "Assets", "Member"]

    with pytest.raises(MisalignedHeadersError):
        TidyData.from_tidy(tidy, tidy2)


def test_tidydata_can_be_written_to_csv(tidy: TidyData):
    """
    Tests that a TidyData objects can be written to a
    csv file via the to_csv method.
    """

    here = Path(__file__).parent
    test_csv_output_path = Path(here / "temporary.csv")
    tidy.to_csv(test_csv_output_path)

    correct_csv_fixture_path: Path = path_to_fixture("csv", "test_output.csv")

    assert_csvs_match(test_csv_output_path, correct_csv_fixture_path)


def test_tidydata_written_to_a_path_indicated_by_a_string(tidy: TidyData):
    """
    Tests that the to_csv method can take a string
    as an argument in place of path.
    """

    output_name = "temp.csv"
    tidy.to_csv(output_name, write_headers=False)

    assert Path(output_name).exists()
    os.remove(output_name)


def test_tidydata_to_csv_raises_for_incorrect_types_for_output_path(tidy: TidyData):
    """
    Confirm the exception is raised where incorrect types
    are passed in for the output destination.
    """

    for wrong_type in [True, 1, None, False]:
        with pytest.raises(ValueError):
            tidy.to_csv(wrong_type)


def test_tidydata_to_csv_raises_specifying_a_non_existent_output_directory(
    tidy: TidyData,
):
    """
    Confirm the exception is raised where we specify a directory
    path for an output and that directory path does not exist
    """

    here = Path(__file__).parent
    bad_path = Path(here / str(uuid.uuid4()) / "should-never-exist.csv")
    with pytest.raises(FileNotFoundError):
        tidy.to_csv(bad_path)


def test_create_tidydata_with_condition_column():
    """
    Test a TidyData object can be instantiated with condition columns
    that depend on each other with a strict priority specified.
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

    TidyData(
        observations.label_as("Value"),
        Column(Constant("Genre", "Rock & Roll")),
        Column(Directly("Assets", assets, above)),
        Column(Directly("Member", member, left)),
        Column.horizontal_condition(
            "Condition1", lambda col: col["Member"] + " " + col["Assets"]
        ),
        Column.horizontal_condition(
            "Condition2", lambda col: col["Condition1"] + "foo", priority=1
        ),
        drop=["Condition2"],
    )._transform()


def test_tidydata_converted_to_dict():
    """
    Test a TidyData object can be instantiated with condition columns
    that depend on each other with a strict priority specified.
    """
    selectable_wide_band_tab: Selectable = fixture_wide_band_tab()

    observations = selectable_wide_band_tab.filter(filters.is_numeric).label_as(
        "Observation"
    )
    bands = (
        selectable_wide_band_tab.excel_ref("A3")
        | selectable_wide_band_tab.excel_ref("G3")
    ).label_as("Band")
    assets = selectable_wide_band_tab.excel_ref("2").is_not_blank().label_as("Asset")
    members = (
        (
            selectable_wide_band_tab.excel_ref("B")
            | selectable_wide_band_tab.excel_ref("H")
        )
        .is_not_blank()
        .label_as("Member")
    )

    tidy_data = TidyData(
        observations,
        Column(bands.attach_closest(right)),
        Column(assets.attach_directly(below)),
        Column(members.attach_directly(right)),
    )

    tidy_as_dict = tidy_data.to_dict()

    with open(path_to_fixture("json", "tidydata_to_dict.json")) as f:
        tidy_as_dict_fixture = json.load(f)

    assert tidy_as_dict == tidy_as_dict_fixture

    # Check that table name is inherited from observations
    # during processing
    const = Column.constant("foo", "bar")
    tidy_data = TidyData(observations, Column.constant("foo", "bar"))
    assert const.table == observations.name


def test_drop_duplicates(tidy: TidyData):
    """
    Test that the tidy_data .drop_duplicates() methods
    works as expected.
    """

    tidy._transform()
    tidy2 = copy.deepcopy(tidy)

    # Add a sneaky duplicate line
    tidy2._data.append(tidy._data[1])
    assert len(tidy2._data) != len(tidy._data)
    assert len(tidy2.drop_duplicates()._data) == len(tidy._data)


def test_drop_duplicates_to_path(tidy: TidyData):
    """
    Test that the tidy_data .drop_duplicates() methods
    works as expected when outputting information on
    duplicates to a file.
    """

    tidy._transform()
    tidy2 = copy.deepcopy(tidy)

    # From path
    # ---------
    tidy2._data.append(tidy._data[1])
    tidy2.drop_duplicates(csv_duplicate_path=Path("deleteme.txt"))

    with open("deleteme.txt") as f:
        assert "1,Rock & Roll,Houses,John" in f.read()
    os.remove("deleteme.txt")

    # From path as str
    # ----------------
    tidy2._data.append(tidy._data[1])
    tidy2.drop_duplicates(csv_duplicate_path="deleteme.txt")

    with open("deleteme.txt") as f:
        assert "1,Rock & Roll,Houses,John" in f.read()
    os.remove("deleteme.txt")

def test_add_column(tidy: TidyData):
    """
    Test that the tidy_data .add_column() method works as expected.
    """

    tidy2 = copy.deepcopy(tidy)
    assert len(tidy2.columns) == 3
    tidy2.add_column(Column.constant("NewColumn", "NewValue"))
    assert len(tidy2.columns) == 4

def test_add_column_after_transform_raises(tidy: TidyData):
    """
    Test that the tidy_data .add_column() method raises an error
    if called after the data has been transformed.
    """

    tidy2 = copy.deepcopy(tidy)
    tidy2._transform()
    with pytest.raises(AssertionError):
        tidy2.add_column(Column.constant("NewColumn", "NewValue"))