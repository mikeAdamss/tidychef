from typing import List

import pytest

from pivoter.models.source.cell import Cell
from pivoter.exceptions import InvalidCellObjectError


@pytest.fixture
def cells_with_valid_values() -> List[Cell]:
    return [
        Cell(x=0, y=0, value="foo"),
        Cell(x=0, y=0, value="bar"),
        Cell(x=0, y=0, value="baz"),
        Cell(x=0, y=0, value="   stripme  "),
        Cell(x=0, y=0, value=""),
        Cell(x=0, y=0, value="    "),
        Cell(x=0, y=0, value=None),
    ]


blank_values_not_disregarding_whitespace = ["", None]
default_blank_values = blank_values_not_disregarding_whitespace + ["    "]


@pytest.fixture
def cells_with_invalid_values() -> List[Cell]:
    return [Cell(x=0, y=0, value=7.9), Cell(x=0, y=0, value=True)]


def test_is_blank_on_valid_cell_values(cells_with_valid_values: List[Cell]):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in cells_with_valid_values:
        if cell.value in default_blank_values:
            assert (
                cell.is_blank()
            ), f"cell {cell._as_xy_str()} failing to return as blank"


def test_is_not_blank_on_valid_cell_values(cells_with_valid_values: List[Cell]):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in cells_with_valid_values:
        if cell.value not in default_blank_values:
            assert (
                cell.is_not_blank()
            ), f"cell {cell._as_xy_str()} failing to return as not blank"


def test_is_blank_on_valid_cell_values_without_disregarding_whitespace(
    cells_with_valid_values: List[Cell],
):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in cells_with_valid_values:
        if cell.value in blank_values_not_disregarding_whitespace:
            assert cell.is_blank(
                disregard_whitespace=False
            ), f"cell {cell._as_xy_str()} failing to return as blank where we're not disregarding whitespace."


def test_is_blank_on_invalid_cell_value_types_raises_err(
    cells_with_invalid_values: List[Cell],
):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in cells_with_invalid_values:

        with pytest.raises(InvalidCellObjectError):
            cell.is_blank()


if __name__ == "__main__":
    pytest()
