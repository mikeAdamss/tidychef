"""
TODO - works but messy, rewrite for clarity once we've a comprehensive test
suite in place.
"""

from typing import Dict, List, Union

from datachef.selection.selectable import Selectable
from datachef.utils import cellutils

from ..boundary import Boundary
from .components import HtmlCell, SelectionKeys
from .constants import BLANK_COLOUR, BORDER_COLOUR, INLINE_CSS, WARNING_COLOUR


def get_preview_table_as_html(
    selections: List[Selectable],
    bounded: Union[str, Dict[str, str]],
    with_excel_notations: bool = True,
    border_cells: str = BORDER_COLOUR,
    blank_cells: str = BLANK_COLOUR,
    warning_colour: str = WARNING_COLOUR,
    multiple_selection_warning: bool = True,
) -> str:
    """ """

    selection_keys = SelectionKeys()
    for selection in selections:
        selection: Selectable

        # If the selection is pristine, someone is just
        # previewing the data prior to selections
        if not selection.selections_made():
            continue
        selection_keys.add_selection_key(selection)

    boundary = Boundary(selections, bounded=bounded)
    all_cells: Selectable = selections[0].pcells
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

    # Add an excel style letter row above the preview
    # where requested
    if with_excel_notations:
        row.append(HtmlCell("", border_cells))
        for i in range(boundary.leftmost_point, boundary.rightmost_point + 1):
            letters = cellutils.x_to_letters(i)
            row.append(HtmlCell(letters, border_cells))
        html_cell_rows.append(row)
        row = [HtmlCell(last_y + 1, border_cells)]

    for cell in all_cells:
        if cell.y != last_y:
            html_cell_rows.append(row)
            if with_excel_notations:
                row = [HtmlCell(cell.y + 1, border_cells)]
            else:
                row = []
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
