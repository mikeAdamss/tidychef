from dataclasses import dataclass

from datachef.against.implementations.base import BaseValidator
from datachef.models.source.cell import Cell


@dataclass
class IsNumericValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a datachef
    Cell object.
    """

    def __call__(self, cell: Cell) -> bool:
        """
        Is the value property of the Cell
        numeric

        :param cell: A single datachef Cell object.
        :return: bool, is it valid or not
        """
        return cell.value.isnumeric()

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        is not numeric

        :param cell: A single datachef Cell object.
        :return: A contextual message
        """

        return f'"{cell.value}" is not numeric'


@dataclass
class IsNotNumericValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a datachef
    Cell object.
    """

    def __call__(self, cell: Cell) -> bool:
        """
        Is the value property of the Cell
        numeric

        :param cell: A single datachef Cell object.
        :return: bool, is it valid or not
        """
        return not cell.value.isnumeric()

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        is numeric

        :param cell: A single datachef Cell object.
        :return: A contextual message
        """

        return f'"{cell.value}" is numeric'
