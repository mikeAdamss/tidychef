from dataclasses import dataclass
from typing import Dict, List

from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from .constants import COLOURS


class SelectionKey:
    """
    A coloured key denoting a single selection
    """

    def __init__(self, selection: Selectable, colour_choice: int):
        """
        Creates a mapping between a colour choice
        and a named selection of cells.

        :param selection: A populated datachef seletable
        or inheritor of.
        :param colour_choice: An integer specifying a colour
        from the constant list COLOURS
        """
        self.label = (
            selection._label
            if selection._label
            else f"Unnamed Selection: {colour_choice}"
        )
        self.colour = COLOURS[colour_choice]
        self.cells = selection.cells

    def matches_xy_of_cell(self, cell: Cell):
        """
        Is the provided datachef Cell present in the
        selection of cells represented by this colour.

        :param cell: A single datachef Cell object.
        """
        cells = [x for x in self.cells if x.x == cell.x and x.y == cell.y]
        return len(cells) == 1

    def as_html(self):
        """
        Create a html table entry identifying this key in previews.
        """
        return f"""
            <tr>
                <td style="background-color:{self.colour}">{self.label}</td>
            <tr>
        """


class SelectionKeys:
    """
    A holding class for constructing and iterating through multiple
    SelectionKey classes.
    """
    def __init__(self):
        self.colour_choice = 0
        self._keys: List[SelectionKey] = []

    def add_selection_key(self, selection: Selectable):
        """
        Add a single SelectionKey to SelectionKeys

        :param selection: The single datachef selectable or
        inheritor of that is represented by a single colour.
        """
        self._keys.append(SelectionKey(selection, self.colour_choice))
        self.colour_choice += 1

    def __iter__(self):
        """
        Iterates through the keys.
        """
        for selection_key in self._keys:
            yield selection_key


class HtmlCell:
    """
    Class to create a simple html representation of a single cell
    using a single background colour.
    """

    def __init__(self, value: str, colour: str):
        """
        Class to create a simple html representation of a single cell
        using a single background colour.
        
        :param value: The value contained in the cell in question.
        :param colour: The background colour to use for the cell.
        """
        self.value = value
        self.colour = colour

    def as_html(self):
        """
        Create the html representation of this cell.
        """
        return f'<td style="background-color:{self.colour}">{self.value}</td>'
