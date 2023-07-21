import pytest

from datachef.exceptions import (
    InvalidCellObjectError,
    InvlaidCellPositionError,
    NonExistentCellComparissonError,
)
from datachef.models.source.cell import Cell, VirtualCell
from datachef.selection.csv.csv import CsvSelectable
from tests.fixtures import fixture_with_blanks

blank_values_not_disregarding_whitespace = [""]
default_blank_values = blank_values_not_disregarding_whitespace + ["    ", " "]


@pytest.fixture
def table_with_blanks():
    return fixture_with_blanks()


def test_is_blank_on_valid_cell_values(table_with_blanks: CsvSelectable):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in table_with_blanks.cells:
        if cell.value in default_blank_values:
            assert (
                cell.is_blank()
            ), f"cell {cell._as_xy_str()} was expected to be but is not blank"


def test_is_not_blank_on_valid_cell_values(table_with_blanks: CsvSelectable):
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
    table_with_blanks: CsvSelectable,
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
    table_with_blanks: CsvSelectable,
):
    """
    Confirm that the truthy blank value of a cell with an
    unsupported type as value raises the appropriate error.
    """

    for cell in table_with_blanks.cells[:1]:

        with pytest.raises(InvalidCellObjectError):
            cell.value = 0.5
            cell.is_blank()


def test_none_counts_as_blank():
    """
    Test that should be define a cell as None it registers
    as blank.
    """
    assert Cell(x=0, y=0, value=None).is_blank()


def test_cell_xy_str():
    """
    Test our cells can print a simple self reference
    """
    assert Cell(x=0, y=0, value="foo")._as_xy_str() == 'x:0, y:0, value = "foo"'


def test_cell_repr():
    """
    Test the default cell repr returns as expected
    """
    assert str(Cell(x=0, y=0, value="foo")) == '(A1, value:"foo", x:0, y:0)'
    assert str(Cell(x=1, y=10, value="bar")) == '(B11, value:"bar", x:1, y:10)'


def test_virt_cell_positional_err():
    """
    Confirm the appropriate error is raised where we are trying to use
    a virtual cell for a positional comparison
    """

    vcell = VirtualCell(value="foo")
    with pytest.raises(NonExistentCellComparissonError):
        vcell.is_right_of("_")


def test_cannot_excel_reference_invalid_cells():
    """
    Make sure that if we have an invalid or missing cell
    position an appropriate error is raised.
    """

    cell = Cell(x=0, y=None, value="foo")
    with pytest.raises(InvlaidCellPositionError):
        cell._excel_ref()


def test_excel_row_and_column():
    """
    Make sure that a cell has a working and accurate
    row and column property.
    """

    cell = Cell(x=0, y=0, value="foo")
    assert cell.excel_column == "A"
    assert cell.excel_row == 1


def test_virt_cell_excel_ref():
    """
    The excel ref of a virtual cell should not error but
    neither should it return an excel reference.
    """
    vcell = VirtualCell(value="foo")
    assert vcell._excel_ref() == "VIRTUAL CELL"


def test_virt_cell_repr():
    """
    The __repr__ a virtual cell should not error but
    neither should it return an excel reference.
    """
    vcell = VirtualCell(value="foo")
    assert str(vcell) == '(VIRTUAL CELL, value:"foo")'
