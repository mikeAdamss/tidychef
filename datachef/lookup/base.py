from abc import ABCMeta, abstractmethod

from datachef.models.source.cell import Cell


class BaseLookupEngine(metaclass=ABCMeta):
    """
    The base class all lookup engines are built upon.
    """

    label: str

    @abstractmethod
    def resolve(self, cell: Cell, *args) -> Cell:
        """
        Given a single observation cell, resolve
        the lookup, returning the relevant cell
        value as defined by this visual relationship.
        """
