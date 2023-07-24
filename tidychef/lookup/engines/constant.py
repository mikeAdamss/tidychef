from tidychef.models.source.cell import Cell, VirtualCell

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

        :param label: The label of the column informed
        by this lookup engine.
        :param value: The constant value we want this
        lookup engine to return.
        """
        self.cell = VirtualCell(value=value)
        self.label = label

    def resolve(self, _: Cell):
        """
        Regardless of the observation cell,
        return the constant cell.

        :param _: Unused Cell object required to keep api
        signature in keeping with the other engines
        """
        return self.cell
