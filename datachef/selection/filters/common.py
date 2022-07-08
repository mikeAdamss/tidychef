"""
Common filters.
"""

from dataclasses import dataclass

from datachef.models.source.cell import Cell


@dataclass
class ContainsString:
    """
    A filter than when given a string, filtlers cells based on whether
    that string appears in the cells value.
    """

    substr: str

    def __call__(self, cell: Cell):
        return self.substr in cell.value


def is_numeric(cell: Cell):
    """
    The value of the cell is numerical
    """
    return cell.value.strip().isnumeric()


def is_not_numeric(cell: Cell):
    """
    The value of the cell is not numerical
    """
    return not cell.value.strip().isnumeric()
