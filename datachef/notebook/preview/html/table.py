"""
TODO - works but messy, rewrite for clarity once we've a comprehensive test
suite in place.
"""

from typing import List, Optional
from datachef.selection.selectable import Selectable
from ..boundary import Boundary
from .components import SelectionKeys, HtmlCell


# Simple CSS to make it pretty-ish
INLINE_CSS = """
    <style>
    table, th, td {
        border: 1px solid;
    }

    table {
        border-collapse: collapse;
    }

    td {
        align: center;
        border: 1px  black solid !important;
        color: black !important;
    }

    th, td {
        padding: 5px;
    }

    </style>
    """

def get_preview_table_as_html(
    selections: List[Selectable],
    with_excel_ref: bool = True,
    start: Optional[str] = None,
    end: Optional[str] = None,
    multiple_selection_warning: bool = True,
) -> str:
    """
    
    """

    selection_keys = SelectionKeys()
    for selection in selections:

        # If the selection is pristine, someone is just previewing the data
        # prior to selections
        if len(selection.cells) == len(selection.pcells):
            continue
        selection_keys.add_selection_key(selection)

    boundary = Boundary(selections, start=start, end=end)
    all_cells: Selectable = selections[0].pcells
    all_cells = [cell for cell in all_cells if
                 cell.x >= boundary.leftmost_point and
                 cell.x <= boundary.rightmost_point and
                 cell.y >= boundary.highest_point and
                 cell.y <= boundary.lowest_point]

    html_cell_rows = []
    last_y = 0
    row = []

    for cell in all_cells:
        if cell.y != last_y:
            html_cell_rows.append(row)
            row = []
            last_y = cell.y

        found = 0
        for selection_key in selection_keys:
            if selection_key.matches_xy_of_cell(cell):
                found += 1
                colour = selection_key.colour

        if found == 1:
            row.append(
                HtmlCell(cell.value, colour=colour)
            )
        elif found > 1:
            selection_keys.show_warning = True
            row.append(
                HtmlCell(cell.value, colour=selection_keys.warning_colour)
            )
        else:
            row.append(
                HtmlCell(cell.value)
            )
    # final row
    html_cell_rows.append(row)

    # ---------------------
    # Create html key table

    if selection_keys.show_warning:
        key_table_html = f"""
            <tr>
                <td style="background-color:{selection_keys.warning_colour}">Cell Appears in Multiple Selections</td>
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
        row_as_html = ''.join([x.as_html() for x in row])
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
                <h2>{selections[0]._name if selections[0]._name else "Unnamed Table"}</h2>
                <table>
                    {cell_table_row_html}
                </table>
            </body>
        </html>
    """


    







