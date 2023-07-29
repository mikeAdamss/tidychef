import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional

from tidychef.against.implementations.base import BaseValidator
from tidychef.models.source.cell import Cell


@dataclass
class RegexValidator(BaseValidator):
    pattern: str
    _compiled: Optional[Pattern] = None

    def __call__(self, cell: Cell) -> bool:
        """
        Does the value property of the Cell
        match the provided pattern.

        :param cell: A single tidychef Cell object.
        :return: bool, is it valid or not
        """
        if self._compiled is None:
            self._compiled = re.compile(r"" + self.pattern)
        if self._compiled.match(cell.value):
            return True
        return False

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        value does not match the provided
        regular expression.

        :param cell: A single tidychef Cell object.
        :return: A contextual message
        """
        return f'"{cell.value}" does not match pattern: "{self.pattern}"'
