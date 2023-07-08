from dataclasses import dataclass
from typing import List

from datachef.models.source.cell import Cell
from datachef.against.implementations.base import BaseValidator

@dataclass
class ItemsValidator(BaseValidator):
    items: List[str]
    
    def __call__(self, cell: Cell) -> bool:
        """
        Does the value property of the Cell
        appear in the items list
        """
        return cell.value in self.items
    
    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        value not on the provided items list
        """

        # dont output the full list if its
        # impractically long.
        if len(self.items) < 11:
            return f'"{cell.value}" not in list: {self.items}'
        else:
            return f'"{cell.value}" not in list.'
