"""
Convenience wrappers for pre defined validators
"""

from typing import List

from .implementations.items import ItemsValidator
from .implementations.regex import RegexValidator


def regex(pattern: str) -> RegexValidator:
    """
    Creates a RegexValidator to check if the
    datachef Cell.value property of a given Cell
    matches the provided pattern.
    """
    return RegexValidator(pattern)


def items(items: List[str]) -> ItemsValidator:
    """
    Creates an ItemsValidator to check if the
    datachef Cell.value property of a given Cell
    is contained within the provided list.
    """
    return ItemsValidator(items)
