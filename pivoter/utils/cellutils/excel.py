from dataclasses import dataclass
import re
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

# TODO - this is nasty and shouldn't be capped, rewrite it
def x_to_letters(x: int) -> str:
    """
    Convert an x co-ordinate to excel style letter references
    """
    full_alphabets = 0
    if x > 26:
        full_alphabets = x / 26
        x -= (full_alphabets * 26)

    if full_alphabets < 27:
        raise NotADirectoryError('Up to 702 columns only supported')

    if full_alphabets > 0:
        return f'{UPPER_ALPHABET[x-1]}:{UPPER_ALPHABET[full_alphabets -1]}'
    return UPPER_ALPHABET[x-1]


def number_to_y(excel_number_ref: int):
    """
    Given an excel row number, return the y offset
    """
    return excel_number_ref - 1  # We are 0 indexed, unlike excel


def single_excel_ref_to_basecells(excel_ref: str) -> List[BaseCell]:
    """
    Given a single excel cell reference, return a list of
    one BaseCell of Cell.

    It's a list to keep the return signature syncronised with the other
    handlers
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

    return [BaseCell(letter_to_x(letters), number_to_y(number))]


def multi_excel_ref_to_basecells(excel_ref: str) -> List[BaseCell]:
    """
    Given an excel reference referring to multiple cells, return a list of
    wanted BaseCells or Cells.
    """

    assert ":" in excel_ref
    start_cell = single_excel_ref_to_basecells(excel_ref.split(":")[0])[0]
    end_cell = single_excel_ref_to_basecells(excel_ref.split(":")[1])[0]

    start_x = start_cell.x
    start_y = start_cell.y
    end_x = end_cell.x
    end_y = end_cell.y

    return_cells = []
    for x in range(start_x, end_x+1):
        for y in range(start_y, end_y+1):
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
        regex = '^[A-Z]+[0-9]+$',
        handler = single_excel_ref_to_basecells
    ),
    "multi_cell": HandlerMatcher(
        regex = '^[A-Z]+[0-9]+:[A-Z]+[0-9]+$',
        handler = multi_excel_ref_to_basecells
    )}
    

def get_ref_as_wanted_basecells(excel_ref: str) -> List[BaseCell]:

    identified_ref_styles = []

    for name, style in ref_styles.items():
        if re.match(style.regex, excel_ref):
            identified_ref_styles.append(name)

    assert len(identified_ref_styles) == 1, (
        f'Identified {len(identified_ref_styles)} styles of excel reference from '
        'ref. 1 is required.' 
    )

    identified_ref_style = identified_ref_styles[0]
    handler = ref_styles[identified_ref_style].handler

    return handler(excel_ref)


def basecells_to_excel_refs(base_cells: List[BaseCell]) -> List[str]:
    """
    Given a list of Basecell, use the BaseCell x and y properties
    to return a list of excel cell references.
    """
    excel_refs = []

    for base_cell in base_cells:
        letters = x_to_letters(base_cell.x)
        number = base_cell.y + 1
        excel_refs.append(f'{letters}:{number}')

    return excel_refs
