"""
Data functions related to excel referencing of x.y positioned cells.
"""
import re
from typing import List

import tidychef.datafuncs.common as dfccommon
from tidychef.exceptions import BadExcelReferenceError, ReversedExcelRefError
from tidychef.models.source.cell import BaseCell
from tidychef.utils import cellutils


def assert_excel_ref_within_cells(cells: List[BaseCell], excel_ref: str):
    """
    Given a list of cells, assert that the cell denoted by
    the provided excel reference, exists within the list.

    :param cells: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :param excel_ref: A single excel reference for a single cell.
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

    :param excel_ref: A excel style reference to one or more cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """

    # Single style reference, eg: A6, ZA18 etc
    if re.match("^[A-Z]+[0-9]+$", excel_ref):
        return [single_excel_ref_to_basecell(excel_ref)]

    # Multi style reference, eg: A1:Z78, G15:AV16 etc
    if re.match("^[A-Z]+[0-9]+:[A-Z]+[0-9]+$", excel_ref):
        return multi_excel_ref_to_basecells(excel_ref)

    raise BadExcelReferenceError(
        f"Could not identify style of excel reference {excel_ref}"
    )


def single_excel_row_to_y_index(excel_ref: str) -> int:
    """
    Given a single row number as an excel reference, return
    the y offset value

    :param excel_ref: A number representing an excel style
    reference to a single row in a tabulated data source.
    :return: y (vertical offset) value.
    """
    return cellutils.number_to_y(int(excel_ref))


def single_excel_column_to_x_index(excel_ref: str) -> str:
    """
    Given a single column latter as an excel reference, return
    the x index.

    :param excel_ref: One or more letters representing an excel
    style reference to a single column in a tabulated source.
    :return: x (horizontal offset) value.
    """
    return cellutils.letters_to_x(excel_ref)


def single_excel_ref_to_basecell(excel_ref: str) -> BaseCell:
    """
    Given a single excel cell reference, return a single BaseCell
    or inheritor of.

    :param excel_ref: A excel style reference to a single cell.
    :return: A BaseCell or inheritor of.
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

    x_index = cellutils.letters_to_x(letters)
    y_index = cellutils.number_to_y(number)

    return BaseCell(x=x_index, y=y_index)


def multi_excel_ref_to_basecells(excel_ref: str) -> List[BaseCell]:
    """
    Given an excel reference referring to multiple cells, return a list of
    wanted BaseCells.

    :param excel_ref: A excel style reference to a range of cells.
    :return: A list of BaseCell or inheritors of that represents a selection
    of cells.
    """

    assert (
        ":" in excel_ref
    ), """
        A multi cell excel reference should be in the format:
        <letter(s)><number>:<letter(s)><number>

        {excel_ref} is missing a colon, ":"
    """
    start_cell = single_excel_ref_to_basecell(excel_ref.split(":")[0])
    end_cell = single_excel_ref_to_basecell(excel_ref.split(":")[1])

    if start_cell.x > end_cell.x or start_cell.y > end_cell.y:
        raise ReversedExcelRefError(
            """
            Invalid excel reference format. Please provide your reference in the
            standard upmost left to downmost right format, i.e A1:C5 not C5:A1
                """
        )

    start_x = start_cell.x
    start_y = start_cell.y
    end_x = end_cell.x
    end_y = end_cell.y

    return_cells = []
    for x_index in range(start_x, end_x + 1):
        for y_index in range(start_y, end_y + 1):
            return_cells.append(BaseCell(x=x_index, y=y_index))

    return return_cells


def basecell_to_excel_ref(cell: BaseCell) -> str:
    """
    Given a single BaseCell object, return the representative excel reference.

    :param: A single BaseCell or inheritor of
    :return: A excel style reference to a single cell.
    """
    return f"{cellutils.x_to_letters(cell.x)}{cellutils.y_to_number(cell.y)}"


def basecells_to_excel_ref(cells: List[BaseCell]) -> str:
    """
    Given a list of cells representing a solid selection with
    no gaps. Return the representative excel reference.

    :param: A list of BaseCell or inheritors of that represents a selection
    of cells.
    :return: A excel style reference to multiple cells.
    """

    min_x, max_x, min_y, max_y = dfccommon.assert_quadrilaterals(cells)

    topleft_cell = dfccommon.specific_cell_from_xy(cells, min_x, min_y)
    bottomright_cell = dfccommon.specific_cell_from_xy(cells, max_x, max_y)

    ref1 = f"{cellutils.x_to_letters(topleft_cell.x)}{cellutils.y_to_number(topleft_cell.y)}"
    ref2 = (
        f"{cellutils.x_to_letters(bottomright_cell.x)}"
        f"{cellutils.y_to_number(bottomright_cell.y)}"
    )
    return f"{ref1}:{ref2}"
