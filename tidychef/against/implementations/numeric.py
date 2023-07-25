from dataclasses import dataclass

from tidychef.against.implementations.base import BaseValidator
from tidychef.models.source.cell import Cell


class IsNumericOrFloatValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a tidychef
    Cell object.
    """

    def __call__(self, cell: Cell) -> bool:
        """
        Is the value property of the Cell
        numeric to include floats

        :param cell: A single tidychef Cell object.
        :return: bool, is it valid or not
        """
        if len(cell.value) > 0:
            if cell.value[0] == ".":
                return False
            if cell.value[-1] == ".":
                return False
        return cell.value.replace(".", "").isnumeric()

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        is not numeric to include floats

        :param cell: A single tidychef Cell object.
        :return: A contextual message
        """

        return f'"{cell.value}" is not numeric or a float'


class IsNotNumericOrFloatValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a tidychef
    Cell object.
    """

    def __call__(self, cell: Cell) -> bool:
        """
        Is the value property of the Cell
        not numeric to include floats

        :param cell: A single tidychef Cell object.
        :return: bool, is it valid or not
        """
        if len(cell.value) > 0:
            if cell.value[0] == ".":
                return True
            if cell.value[-1] == ".":
                return True
        return not cell.value.replace(".", "").isnumeric()

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        is not numeric to include floats

        :param cell: A single tidychef Cell object.
        :return: A contextual message
        """

        return f'"{cell.value}" is numeric or a float'


class IsNotNumericValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a tidychef
    Cell object.
    """

    def __call__(self, cell: Cell) -> bool:
        """
        Is the value property of the Cell
        not numeric

        :param cell: A single tidychef Cell object.
        :return: bool, is it valid or not
        """
        return not cell.value.isnumeric()

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        is numeric

        :param cell: A single tidychef Cell object.
        :return: A contextual message
        """

        return f'"{cell.value}" is numeric'


class IsNumericValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a tidychef
    Cell object.
    """

    def __call__(self, cell: Cell) -> bool:
        """
        Is the value property of the Cell
        numeric

        :param cell: A single tidychef Cell object.
        :return: bool, is it valid or not
        """
        return cell.value.isnumeric()

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        is numeric

        :param cell: A single tidychef Cell object.
        :return: A contextual message
        """

        return f'"{cell.value}" is not numeric'
