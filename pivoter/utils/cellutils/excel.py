import logging
import re
from dataclasses import dataclass
from typing import List

from pivoter.models.source.cell import BaseCell

# TODO: there's a helper for this
UPPER_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def letter_to_x(excel_letters_ref: str) -> int:
    """
    Given letters (as per excel column references), return the equivilent
    x co-ordinate
    """

    # Account for bad conventions
    excel_letters_ref = excel_letters_ref.upper()

    x = 0

    # Account for full iterations of the alphabet,
    # i.e AB, AAB, AH etc
    if len(excel_letters_ref) > 1:
        x = 26 * (len(excel_letters_ref) - 1)
        excel_letters_ref = excel_letters_ref[-1]

    for i, letter in enumerate(UPPER_ALPHABET):
        if letter == excel_letters_ref:
            x += i
            break

    return x


def x_to_letters(x: int) -> str:
    """
    Convert an x co-ordinate to excel style letter references
    """

    # https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
    start_index = 0  #  it can start either at 0 or at 1
    letter = ""
    while x > 25 + start_index:
        letter += chr(65 + int((x - start_index) / 26) - 1)
        x = x - (int((x - start_index) / 26)) * 26
    letter += chr(65 - start_index + (int(x)))

    return letter


def number_to_y(excel_number_ref: int):
    """
    Given an excel row number, return the y offset
    """
    assert isinstance(excel_number_ref, int)
    return excel_number_ref - 1  # We are 0 indexed, unlike excel


def y_to_number(excel_number_ref: int):
    """
    Given a y offset, return the excel row number
    """
    assert isinstance(excel_number_ref, int)
    return excel_number_ref + 1  # We are 0 indexed, unlike excel


def single_excel_ref_to_basecells(excel_ref: str) -> BaseCell:
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

    x = letter_to_x(letters)
    y = number_to_y(number)

    logging.warning(f"single_excel_ref_to_basecells: {excel_ref} becomes x:{x},y:{y}")
    return BaseCell(x=x, y=y)


def multi_excel_ref_to_basecells(excel_ref: str) -> List[BaseCell]:
    """
    Given an excel reference referring to multiple cells, return a list of
    wanted BaseCells.
    """

    assert ":" in excel_ref
    start_cell = single_excel_ref_to_basecells(excel_ref.split(":")[0])
    end_cell = single_excel_ref_to_basecells(excel_ref.split(":")[1])

    start_x = start_cell.x
    start_y = start_cell.y
    end_x = end_cell.x
    end_y = end_cell.y

    return_cells = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            return_cells.append(BaseCell(x=x, y=y))

    return return_cells


@dataclass
class HandlerMatcher:
    """
    Associates a regex with a specific handler
    """

    regex: str
    handler: callable


ref_styles = {
    "single_cell": HandlerMatcher(
        regex="^[A-Z]+[0-9]+$", handler=single_excel_ref_to_basecells
    ),
    "multi_cell": HandlerMatcher(
        regex="^[A-Z]+[0-9]+:[A-Z]+[0-9]+$", handler=multi_excel_ref_to_basecells
    ),
}


def excel_ref_as_wanted_basecells(excel_ref: str) -> List[BaseCell]:
    """
    Convert an excel reference into a list of BaseCell objects,
    holding the x and y indicies of the cells in question.
    """

    identified_ref_styles = []

    for name, style in ref_styles.items():
        if re.match(style.regex, excel_ref):
            identified_ref_styles.append(name)

    assert len(identified_ref_styles) == 1, (
        f"Identified {len(identified_ref_styles)} styles of excel reference from "
        "ref. 1 is required."
    )

    identified_ref_style = identified_ref_styles[0]
    handler = ref_styles[identified_ref_style].handler

    # the single excel ref handler returns a single cell
    # so listify return where necessary
    cell_or_cell_list = handler(excel_ref)
    if not isinstance(cell_or_cell_list, list):
        return [cell_or_cell_list]
    return cell_or_cell_list
