import logging
from typing import List, Union

from tidychef.models.source.cell import Cell
from tidychef.models.source.table import LiveTable

from .constants import COLOURS

logger = logging.getLogger(__name__)

class SelectionKey:
    """
    A coloured key denoting a single selection
    """

    def __init__(self, selection: LiveTable, colour_choice: int):
        """
        Creates a mapping between a colour choice
        and a named selection of cells.

        :param selection: A populated tidychef seletable
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
        Is the provided tidychef Cell present in the
        selection of cells represented by this colour.

        :param cell: A single tidychef Cell object.
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

    def add_selection_key(self, selection: LiveTable):
        """
        Add a single SelectionKey to SelectionKeys

        :param selection: The single tidychef selectable or
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
    using a single background colour and optional text formatting.
    """

    def __init__(self, value: Union[str, int, Cell], colour: str, cell: Cell = None):
        """
        Class to create a simple html representation of a single cell
        using a single background colour and optional text formatting.

        :param value: The value contained in the cell, or a Cell object
        :param colour: The background colour to use for the cell.
        :param cell: Optional Cell object for formatting information
        """
        if isinstance(value, Cell):
            self.cell = value
            self.value = value.value
        else:
            self.cell = cell
            self.value = str(value)
        self.colour = colour

    def as_html(self):
        """
        Create the html representation of this cell with formatting.
        """
        content = str(self.value)
        
        # Apply text formatting if cell formatting is available
        if self.cell and self.cell.cellformat:
            # Check for hyperlink first (higher priority than underline)
            is_hyperlink = False
            try:
                if self.cell.cellformat.is_hyperlink():
                    # Style hyperlinks differently - could be enhanced to include actual href
                    content = f'<span style="color: blue; text-decoration: underline;">{content}</span>'
                    is_hyperlink = True
            except Exception:
                logger.error("Error checking hyperlink formatting", exc_info=True)
            
            try:
                if self.cell.cellformat.is_bold():
                    content = f"<strong>{content}</strong>"
            except Exception:
                logger.error("Error checking bold formatting", exc_info=True)

            try:
                if self.cell.cellformat.is_italic():
                    content = f"<em>{content}</em>"
            except Exception:
                logger.error("Error checking italic formatting", exc_info=True)

            # Only apply underline formatting if it's not a hyperlink
            try:
                if not is_hyperlink and self.cell.cellformat.is_underline():
                    content = f"<u>{content}</u>"
            except Exception:
                logger.error("Error checking underline formatting", exc_info=True)

        return f'<td style="background-color:{self.colour}">{content}</td>'
