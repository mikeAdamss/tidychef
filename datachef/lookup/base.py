from abc import ABCMeta, abstractmethod

from datachef.models.source.cell import Cell


class BaseLookup(metaclass=ABCMeta):
    """
    The base class all engines are built upon.
    """

    def __init__(self, *args, name: str, **kwargs):

        # Always get a compnent name, so we can give
        # meaningful feedback where issues are encountered
        self.name = name
        self._post_init(*args, **kwargs)

    @abstractmethod
    def _post_init(self, *args, **kwargs):
        """
        Use the supplied parameters to construct the
        lookup engine in question.
        """

    @abstractmethod
    def resolve(self, cell: Cell) -> str:
        """
        Given a single observation cell, resolve
        the lookup, returning the relevant cell
        as defined by this visual relationship.
        """
