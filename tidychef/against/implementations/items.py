from dataclasses import dataclass
from typing import List

from tidychef.against.implementations.base import BaseValidator
from tidychef.models.source.cell import Cell


@dataclass
class ItemsValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a tidychef
    Cell object.
    """

    items: List[str]

    def __call__(self, cell: Cell) -> bool:
        """
        Does the value property of the Cell
        appear in the items list

        :param cell: A single tidychef Cell object.
        :return: bool, is it valid or not
        """
        return cell.value in self.items

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        value not on the provided items list

        :param cell: A single tidychef Cell object.
        :return: A contextual message
        """

        # dont output the full list if its
        # impractically long.
        if len(self.items) < 11:
            return f'"{cell.value}" not in list: {self.items}'
        else:
            return f'"{cell.value}" not in list.'
