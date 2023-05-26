from abc import ABCMeta, abstractmethod

from datachef.models.source.cell import Cell


class BaseLookupEngine(metaclass=ABCMeta):
    """
    The base class all engines are built upon.
    """

    @abstractmethod
    def resolve(self, cell: Cell) -> Cell:
        """
        Given a single observation cell, resolve
        the lookup, returning the relevant cell
        value as defined by this visual relationship.
        """
