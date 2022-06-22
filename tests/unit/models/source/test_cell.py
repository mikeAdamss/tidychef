import pytest

from pivoter.exceptions import InvalidCellObjectError
from pivoter.selection.csv.csv import CsvInputSelectable
from tests.fixtures import fixture_with_blanks

blank_values_not_disregarding_whitespace = [""]
default_blank_values = blank_values_not_disregarding_whitespace + ["    ", " "]


@pytest.fixture
def table_with_blanks():
    return fixture_with_blanks()


def test_is_blank_on_valid_cell_values(table_with_blanks: CsvInputSelectable):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in table_with_blanks.cells:
        if cell.value in default_blank_values:
            assert (
                cell.is_blank()
            ), f"cell {cell._as_xy_str()} was expected to be but is not blank"


def test_is_not_blank_on_valid_cell_values(table_with_blanks: CsvInputSelectable):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in table_with_blanks.cells:
        if cell.value not in default_blank_values:
            assert (
                cell.is_not_blank()
            ), f"cell {cell._as_xy_str()} was expected to be but not blank but isn't"


def test_is_blank_on_valid_cell_values_without_disregarding_whitespace(
    table_with_blanks: CsvInputSelectable,
):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in table_with_blanks.cells:
        if cell.value in blank_values_not_disregarding_whitespace:
            assert cell.is_blank(
                disregard_whitespace=False
            ), f"cell {cell._as_xy_str()} failing to return as blank where we're not disregarding whitespace."


def test_is_blank_on_invalid_cell_value_types_raises_err(
    table_with_blanks: CsvInputSelectable,
):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in table_with_blanks.cells[:1]:

        with pytest.raises(InvalidCellObjectError):
            cell.value = 0.5
            cell.is_blank()
