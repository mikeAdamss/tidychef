from abc import ABCMeta, abstractmethod

from datachef.models.source.cell import Cell

class BaseValidator(metaclass=ABCMeta):
    """
    The standard Matcher used to validate a
    single cell object.
    """

    @abstractmethod
    def __call__(self, cell: Cell) -> bool:
        """
        Confirm that a single cell is valid.
        """
        

    @abstractmethod
    def msg(self, cell: Cell) -> str:
        """
        Generate a message on validation failure
        to provide some contextual information to
        the user
        """
        