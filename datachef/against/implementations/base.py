from abc import ABCMeta, abstractmethod

from datachef.models.source.cell import Cell


class BaseValidator(metaclass=ABCMeta):
    """
    The standard Matcher used to provide validation
    of the data being extracted.

    Please note - all Matcher methods should operate
    against a single Cell at a time and throw an
    AssertionError where a Cell is not valid.
    """

    @abstractmethod
    def __call__(self, cell: Cell):
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
        