from typing import Any

from datachef.models.source.cell import Cell, VirtualCell

from ..base import BaseLookupEngine


class Constant(BaseLookupEngine):
    """
    A class to resolve a direct lookup between
    an observation cell and a single constant
    value.
    """

    def __init__(self, label: str, value: str):
        """
        A class to resolve a direct lookup between
        an observation cell and a single constant
        value.
        """
        self.cell = VirtualCell(value=value)
        self.label = label

    def resolve(self, _: Cell):
        """
        Regardless of the observation cell,
        return the constant cell.
        """
        return self.cell
