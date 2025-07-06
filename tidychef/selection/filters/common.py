"""
Common filters.
"""

from dataclasses import dataclass

from tidychef.models.source.cell import Cell


@dataclass
class ContainsString:
    """
    A filter than when given a string, filters cells based on whether
    that string appears in the cell value.
    """

    substr: str

    def __call__(self, cell: Cell):
        return self.substr in cell.value


@dataclass
class NotContainsString:
    """
    A filter than when given a string, filters cells based on whether
    that string does not appear in the cell value.
    """

    substr: str

    def __call__(self, cell: Cell):
        return self.substr not in cell.value


class IsNumeric:
    """
    The value of the cell is numerical
    """
    def __call__(self, cell: Cell):
        return cell.numeric


is_numeric = IsNumeric()


class IsNotNumeric:
    """
    The value of the cell is numerical
    """

    def __call__(self, cell: Cell):
        return not cell.numeric

is_not_numeric = IsNotNumeric()
