from dataclasses import dataclass
from typing import Dict, List

from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable

WARNING_COLOUR = "#ff8080"
COLOURS = [
    "cyan",
    "#99ff99",
    "#eeccff",
    "#ffe066",
    "#ff4da6",
    "#ff9933",
    "#4d4dff",
    "#b3d9ff",
    "#00b3b3",
    "#99ffcc",
    "#b380ff",
]


class SelectionKey:
    """
    A coloured key denoting a single selection
    """

    def __init__(self, selection: Selectable, colour_choice: int):
        self.label = (
            selection._label
            if selection._label
            else f"Unnamed Selection: {colour_choice}"
        )
        self.colour = COLOURS[colour_choice]
        self.cells = selection.cells

    def matches_xy_of_cell(self, cell: Cell):
        cells = [x for x in self.cells if x.x == cell.x and x.y == cell.y]
        return len(cells) == 1

    def as_html(self):
        return f"""
            <tr>
                <td style="background-color:{self.colour}">{self.label}</td>
            <tr>
        """


class SelectionKeys:
    def __init__(self):
        self.colour_choice = 0
        self._keys: List[SelectionKey] = []

        self.show_warning = False
        self.warning_colour = WARNING_COLOUR

    def add_selection_key(self, selection: Selectable):
        self._keys.append(SelectionKey(selection, self.colour_choice))
        self.colour_choice += 1

    def __iter__(self):
        for selection_key in self._keys:
            yield selection_key


class HtmlCell:
    """
    Simple html representation of a single cell
    """

    def __init__(self, value: str, colour="white"):
        self.value = value
        self.colour = colour

    def as_html(self):
        return f'<td style="background-color:{self.colour}">{self.value}</td>'
