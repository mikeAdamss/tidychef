"""
Convenience wrappers for pre defined validators
"""

from typing import List, Optional

from .implementations.items import ItemsValidator
from .implementations.length import LengthValidator
from .implementations.numeric import (
    IsNotNumericOrFloatValidator,
    IsNotNumericValidator,
    IsNumericOrFloatValidator,
    IsNumericValidator,
)
from .implementations.regex import RegexValidator


def regex(pattern: str) -> RegexValidator:
    """
    Creates a RegexValidator to check if the
    tidychef Cell.value property of a given Cell
    matches the provided pattern.

    :param pattern: A regular expression
    :return: A instantiated RegexValidator
    """
    return RegexValidator(pattern)


def items(items: List[str]) -> ItemsValidator:
    """
    Creates an ItemsValidator to check if the
    tidychef Cell.value property of a given Cell
    is contained within the provided list.

    :param items: A list of strings representing valid values
    :return: A instantiated ItemsValidator
    """
    return ItemsValidator(items)


def length(least: Optional[int] = None, most: Optional[int] = None) -> LengthValidator:
    """
    Creates a LengthValidator to check if the
    tidychef Cell.value property of a given Cell
    is with the stated length constraints.

    :param least: The minimum length the cell value must be if any
    :param most: The minimum length the cell value must be if any
    :return: A instantiated LengthValidator
    """
    return LengthValidator(least=least, most=most)


# Pre instantiate these since no arguments are required.
is_numeric = IsNumericValidator()
is_not_numeric = IsNotNumericValidator()
is_not_numeric_or_float = IsNotNumericOrFloatValidator()
is_numeric_or_float = IsNumericOrFloatValidator()
