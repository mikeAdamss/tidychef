"""
Convenience wrappers for pre defined validators
"""

from typing import List

from .implementations.items import ItemsValidator
from .implementations.numeric import IsNotNumericValidator, IsNumericValidator
from .implementations.regex import RegexValidator


def regex(pattern: str) -> RegexValidator:
    """
    Creates a RegexValidator to check if the
    datachef Cell.value property of a given Cell
    matches the provided pattern.

    :param pattern: A regular expression
    :return: A instantiated RegexValidator
    """
    return RegexValidator(pattern)


def items(items: List[str]) -> ItemsValidator:
    """
    Creates an ItemsValidator to check if the
    datachef Cell.value property of a given Cell
    is contained within the provided list.

    :param items: A list of strings representing valid values
    :return: A instantiated ItemsValidator
    """
    return ItemsValidator(items)

# Pre instantiate these since no arguments are required.
is_numeric = IsNumericValidator()
is_not_numeric = IsNotNumericValidator()