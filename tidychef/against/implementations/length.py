from dataclasses import dataclass
from typing import Optional

from tidychef.against.implementations.base import BaseValidator
from tidychef.models.source.cell import Cell


@dataclass
class LengthValidator(BaseValidator):
    """
    A class to return bool (valid or not) when
    called with a single instance of a tidychef
    Cell object.
    """

    least: Optional[int] = None
    most: Optional[int] = None

    def __post_init__(self):
        assert not all([self.least is None, self.most is None]), (
            "To use a length validator you must provide at least one "
            "keyword argument from least= and most="
        )
        if self.least and self.most:
            assert (
                self.most > self.least
            ), f"""
                Your most value needs to be bigger than least,
                you have provided:
                                            
                least: {self.least}
                most: {self.most}
            """
        if self.least:
            assert isinstance(self.least, int), "You least value must be an integer."
        if self.most:
            assert isinstance(self.most, int), "You most value must be an integer."

    def __call__(self, cell: Cell) -> bool:
        """
        Is the length of the value property of the Cell
        between the minimum and maximum length

        :param cell: A single tidychef Cell object.
        :return: bool, is it valid or not
        """
        if self.least and self.most:
            return len(cell.value) >= self.least and len(cell.value) <= self.most
        elif self.least:
            return len(cell.value) >= self.least
        else:
            return len(cell.value) <= self.most

    def msg(self, cell: Cell) -> str:
        """
        Provide a contextually meaningful
        message to the user where cell
        is not numeric

        :param cell: A single tidychef Cell object.
        :return: A contextual message
        """
        if self.least and self.most:
            return f'The length of cell value "{cell.value}" is not between {self.least} and {self.most} in length.'
        elif self.least:
            return f'The length of cell value "{cell.value}" is not above the minimum length of {self.least}.'
        else:
            return f'The length of cell value "{cell.value}" is not below the maximum length of {self.most}.'
