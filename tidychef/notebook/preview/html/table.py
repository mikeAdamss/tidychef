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
    COLOURS,
    MULTIPLE_SELECTION_COLOURS,
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

    # Track multiple selection combinations for enhanced key display
    multiple_selection_combinations = {}  # combination_key -> {'selections': [...], 'cells': [...], 'colour': str}
    combination_colour_index = 0
    
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

        matching_selections = []
        for selection_key in selection_keys:
            if selection_key.matches_xy_of_cell(cell):
                matching_selections.append(selection_key)

        if len(matching_selections) == 1:
            row.append(HtmlCell(cell, matching_selections[0].colour))
        elif len(matching_selections) > 1:
            if multiple_selection_warning:
                # Create a unique key for this combination of selections
                selection_labels = sorted([sel.label for sel in matching_selections])
                combination_key = " + ".join(selection_labels)
                
                if combination_key not in multiple_selection_combinations:
                    # Assign a unique color to this combination from the separate palette
                    # Use colors from MULTIPLE_SELECTION_COLOURS list, cycling through if needed
                    combo_colour = MULTIPLE_SELECTION_COLOURS[combination_colour_index % len(MULTIPLE_SELECTION_COLOURS)]
                    combination_colour_index += 1
                    
                    multiple_selection_combinations[combination_key] = {
                        'selections': matching_selections.copy(),
                        'cells': [],
                        'colour': combo_colour
                    }
                multiple_selection_combinations[combination_key]['cells'].append(cell)
                
                # Use the unique color for this combination
                combo_colour = multiple_selection_combinations[combination_key]['colour']
                row.append(HtmlCell(cell, combo_colour))
                show_warning = True
            else:
                row.append(HtmlCell(cell, matching_selections[0].colour))
        else:
            row.append(HtmlCell(cell, blank_cells))

    # final row
    html_cell_rows.append(row)

    # ---------------------
    # Create html key table with two-column layout

    # Build individual selections column
    individual_selections_html = ""
    for selection_key in selection_keys:
        individual_selections_html += selection_key.as_html()

    # Build multiple selections column (only if there are any)
    multiple_selections_html = ""
    if show_warning and multiple_selection_combinations:
        for combination_key, combination_info in multiple_selection_combinations.items():
            selections = combination_info['selections']
            cell_count = len(combination_info['cells'])
            combo_colour = combination_info['colour']
            
            # Create a visual representation showing which selections are combined
            selection_colors_html = ""
            for sel in selections:
                selection_colors_html += f'<span style="background-color:{sel.colour}; padding: 2px 4px; margin: 1px; display: inline-block;">{sel.label}</span>'
            
            multiple_selections_html += f"""
                <tr>
                    <td style="background-color:{combo_colour}">
                        {combination_key} ({cell_count} cell{'s' if cell_count != 1 else ''}) → {selection_colors_html}
                    </td>
                </tr>
            """

    # Create the key content without outer box, only show if there are selections
    if individual_selections_html or (show_warning and multiple_selection_combinations):
        if show_warning and multiple_selection_combinations:
            # Two-column layout when there are multiple selections
            key_content_html = f"""
                <div style="display: flex; margin-bottom: 15px;">
                    <div style="margin-right: 30px;">
                        <strong style="text-align: left;">Selections</strong>
                        <table style="width: auto; margin-top: 5px; text-align: left;">
                            {individual_selections_html}
                        </table>
                    </div>
                    <div>
                        <strong style="text-align: left;">Multiple Selection Warnings</strong>
                        <table style="width: auto; margin-top: 5px; text-align: left;">
                            {multiple_selections_html}
                        </table>
                    </div>
                </div>
            """
        elif individual_selections_html:
            # Single column layout when there are selections but no multiple selections
            key_content_html = f"""
                <div style="margin-bottom: 15px;">
                    <strong style="text-align: left;">Selections</strong>
                    <table style="width: auto; margin-top: 5px; text-align: left;">
                        {individual_selections_html}
                    </table>
                </div>
            """
        else:
            key_content_html = ""
    else:
        # No selections made, don't show any key content
        key_content_html = ""

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
            <body>
                <h2>{selections[0].name if selections and hasattr(selections[0], 'name') else 'Preview'}</h2>
                
                {key_content_html}
                
                <table>
                    {cell_table_row_html}
                </table>
            </body>
            <br>
        </html>
    """