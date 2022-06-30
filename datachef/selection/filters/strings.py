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
