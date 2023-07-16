import re
from dataclasses import dataclass

from datachef.against.implementations.base import BaseValidator
from datachef.models.source.cell import Cell


@dataclass
class RegexValidator(BaseValidator):
    pattern: str

    def __call__(self, cell: Cell) -> bool:
        """
        Does the value property of the Cell
        match the provided pattern.

        :param cell: A single datachef Cell object.
        :return: bool, is it valid or not
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

        :param cell: A single datachef Cell object.
        :return: A contextual message
        """
        return f'"{cell.value}" does not match pattern: "{self.pattern}"'