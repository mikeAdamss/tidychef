"""
TODO - works but messy, rewrite for clarity once we've a comprehensive test
suite in place.
"""

from typing import List

from tidychef.models.source.table import LiveTable
from tidychef.utils import cellutils

from ..boundary import Boundary
from .components import HtmlCell, SelectionKeys
from .constants import (
    BORDER_CELL_COLOUR,
    BORDER_CELL_SECONDARY_COLOUR,
    INLINE_CSS,
    NO_COLOUR,
    WARNING_COLOUR,
)


def get_preview_table_as_html(
    selections: List[LiveTable],
    bounded: str,
    show_excel: bool = True,
    show_xy: bool = False,
    border_cells: str = BORDER_CELL_COLOUR,
    blank_cells: str = NO_COLOUR,
    warning_colour: str = WARNING_COLOUR,
    border_cell_secondary_colour: str = BORDER_CELL_SECONDARY_COLOUR,
    multiple_selection_warning: bool = True,
    selection_boundary: bool = False,
) -> str:
    """ """

    selection_keys = SelectionKeys()
    for selection in selections:
        selection: LiveTable

        # If the selection is pristine, someone is just
        # previewing the data prior to selections
        if not selection.selections_made() and selection_boundary is False:
            continue
        selection_keys.add_selection_key(selection)

    boundary = Boundary(
        selections, bounded=bounded, selection_boundary=selection_boundary
    )
    all_cells: LiveTable = selections[0].pcells
    all_cells = [
        cell
        for cell in all_cells
        if cell.x >= boundary.leftmost_point
        and cell.x <= boundary.rightmost_point
        and cell.y >= boundary.highest_point
        and cell.y <= boundary.lowest_point
    ]

    html_cell_rows = []
    last_y = boundary.highest_point
    row = []
    show_warning = False

    # Add table headers as needed.
    if show_xy or show_excel:
        if show_xy:
            row.append(HtmlCell("x/y", border_cell_secondary_colour))
            if show_excel:
                row.append(HtmlCell("", border_cell_secondary_colour))
            for i in range(boundary.leftmost_point, boundary.rightmost_point + 1):
                row.append(HtmlCell(i, border_cell_secondary_colour))
            html_cell_rows.append(row)
            row = []

        if show_excel:
            if show_xy:
                row.append(HtmlCell("", border_cell_secondary_colour))
            row.append(HtmlCell("", border_cells))
            for i in range(boundary.leftmost_point, boundary.rightmost_point + 1):
                letters = cellutils.x_to_letters(i)
                row.append(HtmlCell(letters, border_cells))
            html_cell_rows.append(row)
            row = []

        if show_xy:
            row.append(HtmlCell(last_y, border_cell_secondary_colour))
        if show_excel:
            row.append(HtmlCell(last_y + 1, border_cells))

    # Add cell rows, including xy and excel if so indicated
    for cell in all_cells:
        if cell.y != last_y:
            html_cell_rows.append(row)
            row = []
            if show_xy:
                row.append(HtmlCell(cell.y, border_cell_secondary_colour))
            if show_excel:
                row.append(HtmlCell(cell.y + 1, border_cells))
            last_y = cell.y

        found = 0
        for selection_key in selection_keys:
            if selection_key.matches_xy_of_cell(cell):
                found += 1
                colour = selection_key.colour

        if found == 1:
            row.append(HtmlCell(cell.value, colour=colour))
        elif found > 1:
            if multiple_selection_warning:
                row.append(HtmlCell(cell.value, colour=warning_colour))
                show_warning = True
            else:
                row.append(HtmlCell(cell.value, colour=colour))
        else:
            row.append(HtmlCell(cell.value, blank_cells))

    # final row
    html_cell_rows.append(row)

    # ---------------------
    # Create html key table

    if show_warning:
        key_table_html = f"""
            <tr>
                <td style="background-color:{warning_colour}">Cell Appears in Multiple Selections</td>
            <tr>
        """
    else:
        key_table_html = ""

    for selection_key in selection_keys:
        key_table_html += selection_key.as_html()

    # ---------------------
    # Create html cell rows

    cell_table_row_html = ""
    for row in html_cell_rows:
        row: List[HtmlCell]
        row_as_html = "".join([x.as_html() for x in row])
        cell_table_row_html += f"<tr>{row_as_html}</tr>\n"

    # ------------
    # Create tables

    return f"""
    <html>
        {INLINE_CSS}
            <table>
                {key_table_html}
            </table>

            <body>
                <h2>{selections[0].name}</h2>
                <table>
                    {cell_table_row_html}
                </table>
            </body>
            <br>
        </html>
    """
