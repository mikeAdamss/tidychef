import string


def letters_to_x(excel_letters_ref: str) -> int:
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

    for i, letter in enumerate(string.ascii_uppercase):
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
