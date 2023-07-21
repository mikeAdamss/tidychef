"""
Common filters.
"""

from dataclasses import dataclass

from datachef.models.source.cell import Cell


@dataclass
class ContainsString:
    """
    A filter than when given a string, filters cells based on whether
    that string appears in the cell value.
    """

    substr: str

    @property
    def explain(self) -> str:
        return f"Contains string: {self.substr}"

    def __call__(self, cell: Cell):
        return self.substr in cell.value


@dataclass
class NotContainsString:
    """
    A filter than when given a string, filters cells based on whether
    that string does not appear in the cell value.
    """

    substr: str

    @property
    def explain(self) -> str:
        return f"Does not contain string: {self.substr}"

    def __call__(self, cell: Cell):
        return self.substr not in cell.value


class IsNumeric:
    """
    The value of the cell is numerical
    """

    @property
    def explain(self) -> str:
        return "Cell value is numeric"

    def __call__(self, cell: Cell):
        return cell.value.strip().isnumeric()


is_numeric = IsNumeric()


class IsNotNumeric:
    """
    The value of the cell is numerical
    """

    @property
    def explain(self) -> str:
        return "Cell value is not numeric"

    def __call__(self, cell: Cell):
        return not cell.value.strip().isnumeric()


is_not_numeric = IsNotNumeric()
