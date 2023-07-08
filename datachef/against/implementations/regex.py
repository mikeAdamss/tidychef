import re
from dataclasses import dataclass

from datachef.models.source.cell import Cell
from datachef.against.implementations.base import BaseValidator

@dataclass
class RegexValidator(BaseValidator):
    pattern: str
    
    def __call__(self, cell: Cell) -> bool:
        """
        Does the value property of the Cell
        match the provided pattern
        """
        if re.match(self.pattern, cell.value):
            return True
        return False
    
    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        value does not match the provided
        regular expression.
        """
        return f'"{cell.value}" does not match pattern: "{self.pattern}"'
