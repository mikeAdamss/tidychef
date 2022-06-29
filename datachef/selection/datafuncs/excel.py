import re
from typing import List

from datachef.exceptions import BadExcelReferenceError, ReversedExcelRefError
from datachef.models.source.cell import BaseCell
from datachef.utils import cellutils

from . import common as dfccommon


def assert_excel_ref_within_cells(cells: List[BaseCell], excel_ref: str):
    """
    Given a list of cells, assert that the cell denoted by
    the provided excel reference, exists within the list
    """
    wanted_cell: BaseCell = single_excel_ref_to_basecell(excel_ref)
    match = [c1 for c1 in cells if any([c1.matches_xy(wanted_cell)])]
    assert (
        len(match) == 1
    ), f"Cell of excel ref {excel_ref} is not contained in the provided selection"


def any_excel_ref_as_wanted_basecells(excel_ref: str) -> List[BaseCell]:
    """
    Convert an excel reference of either the single or multiple cell
    format into a list of BaseCell objects.
    """

    # Single style reference, eg: A6, ZA18 etc
    if re.match("^[A-Z]+[0-9]+$", excel_ref):
        return [single_excel_ref_to_basecell(excel_ref)]

    # Multi style reference, eg: A1:Z78, G15:AV16 etc
    elif re.match("^[A-Z]+[0-9]+:[A-Z]+[0-9]+$", excel_ref):
        return multi_excel_ref_to_basecells(excel_ref)
    else:
        raise BadExcelReferenceError(
            f"Could not identify style of excel reference {excel_ref}"
        )


def single_excel_ref_to_basecell(excel_ref: str) -> BaseCell:
    """
    Given a single excel cell reference, return a single BaseCell.
    """

    letters = ""
    number = None
    for i, letter_or_num in enumerate(excel_ref):
        try:
            int(letter_or_num)
            number = int(excel_ref[i:])
            break
        except ValueError:
            letters += letter_or_num

    assert number
    assert len(letters) > 0

    x = cellutils.letters_to_x(letters)
    y = cellutils.number_to_y(number)

    return BaseCell(x=x, y=y)


def multi_excel_ref_to_basecells(excel_ref: str) -> List[BaseCell]:
    """
    Given an excel reference referring to multiple cells, return a list of
    wanted BaseCells.
    """

    assert ":" in excel_ref
    start_cell = single_excel_ref_to_basecell(excel_ref.split(":")[0])
    end_cell = single_excel_ref_to_basecell(excel_ref.split(":")[1])

    if start_cell.x > end_cell.x or start_cell.y > end_cell.y:
        raise ReversedExcelRefError()

    start_x = start_cell.x
    start_y = start_cell.y
    end_x = end_cell.x
    end_y = end_cell.y

    return_cells = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            return_cells.append(BaseCell(x=x, y=y))

    return return_cells


def xycell_to_excel_ref(cell: BaseCell) -> str:
    """
    Given a single BaseCell object, return the representative excel reference.
    """
    return f"{cellutils.x_to_letters(cell.x)}{cellutils.y_to_number(cell.y)}"


def xycells_to_excel_ref(cells: List[BaseCell]) -> str:
    """
    Given a list of cells representing a solid selection with
    no gaps. Return the representative excel reference.
    """

    min_x, max_x, min_y, max_y = dfccommon.assert_quadrilaterals(
        cells, return_outlier_indicies=True
    )

    topleft_cell = dfccommon.specific_cell_from_xy(cells, min_x, min_y)
    bottomright_cell = dfccommon.specific_cell_from_xy(cells, max_x, max_y)

    ref1 = f"{cellutils.x_to_letters(topleft_cell.x)}{cellutils.y_to_number(topleft_cell.y)}"
    ref2 = f"{cellutils.x_to_letters(bottomright_cell.x)}{cellutils.y_to_number(bottomright_cell.y)}"
    return f"{ref1}:{ref2}"
