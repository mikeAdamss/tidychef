"""
TODO - works but messy, rewrite for clarity once we've a comprehensive test
suite in place.
"""

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from IPython.display import HTML, display

from datachef.exceptions import UnnamedTableError
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable
from datachef.utils import cellutils

from ..base import BasePreview
from ..boundary import Boundary


class HtmlPreview(BasePreview):
    """
    Class representing a html previewed selection.
    """

    def _make_preview_as_html_str(
        self,
        selections: List[Selectable],
        with_excel_ref: bool = True,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> str:

        boundary = Boundary(selections, start=start, end=end)

        # Keep track of colours based on selection in question
        palette = {}
        for i, colour in enumerate(
            [
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
        ):
            palette[i] = colour

        warning_colour = "#ff8080"
        warning_used = False

        inline_css = """
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

        doc = """
        <html>
        {style}
            <table>
                {key_rows}
            </table>

            <body>
                <h2>{title}</h2>
                {table}
            </body>
        </html>
        """

        key_row = """
            <tr>
                <td style="background-color:{colour}">{value}</td>
            <tr>
        """

        table = """
            <table>
                {rows}
            </table>
        """

        tr = "<tr>{row}</tr>"

        td_unselected = "<td>{value}</td>"
        td_selected = '<td style="background-color:{colour}">{value}</td>'

        all_cells: List[Cell] = dfc.order_cells_leftright_topbottom(selections[0].pcells)

        # ------------------
        # Cell lookup logic
        # (for now, this needs to be reworked)
        #
        # The below three principle things
        #
        # master_selected_cells_index: {
        #         <arbitrary index for a selection> : <ordered list of cells in that selection>
        # }
        #
        # get_next_selected_cell()   <- function
        # when passed an index pops and returns the next cell from the dict explained above.
        #
        # looked_for_cells {
        #         <arbitrary index for a selction> : <the NEXT UNUSED cell in this selectio>
        # }
        #
        # It needs some cleaning up, but simply put:
        # 1. ) We used looked_for_cells to check if the cell being written to the preview is a
        #     selected cell (as we consider each cell of the table in turn to build the preview).
        # 2.) We use master_selected_cells_index and get_next_selected_cell() to update looked_for_cells
        #     whenever a selected cell is written to the preview, so at all times it holds
        #     the next cell due to appear for every selection.

        key_rows = ""
        master_selected_cells_index = {}
        for i, s in enumerate(selections):
            master_selected_cells_index[i] = deque(dfc.order_cells_leftright_topbottom(s.cells))
            key_rows += key_row.format(
                colour=palette[i], value=s._label if s._label else f"selection {i}"
            )

        def get_next_selected_cell(i: int) -> Cell:
            next_cell = master_selected_cells_index[i].popleft()
            return next_cell

        looked_for_cells = {}
        for i in master_selected_cells_index.keys():
            looked_for_cells[i] = get_next_selected_cell(i)

        # -------------------
        # Html generation logic
        # (for now, this needs to be reworked)
        #
        # 1.) Starting with a "row" (a blank string)
        # 2.) Iterate through the cells building up the html to represent the row
        # 4.) Append to the list "rows"

        rows = []
        row = ""
        row_no = 0

        # This logic is just for creating a excel style header
        # row, where the user hasn't specified not to
        if with_excel_ref:
            row += td_unselected.format(value="")
            for cell in all_cells:
                if cell.y == row_no:
                    if cell.x > boundary.rightmost_point:
                        continue
                    if cell.x < boundary.leftmost_point:
                        continue
                    row += td_unselected.format(value=cellutils.x_to_letters(cell.x))
                else:
                    rows.append(tr.format(row=row))
                    row = ""

                    # Add the row number if appropriate
                    if boundary.contains(cell) and with_excel_ref:
                        row += td_unselected.format(value=cell.y)
                    break

        for cell in all_cells:
            if cell.y != row_no:
                if cell.y > boundary.lowest_point:
                    break
                row_no += 1
                rows.append(tr.format(row=row))
                row = ""
                if all(
                    [
                        with_excel_ref,
                        cell.y >= boundary.highest_point,
                        cell.y <= boundary.lowest_point,
                    ]
                ):
                    row += td_unselected.format(value=cell.y + 1)

            # If one of our selected cells matches the cell being considered
            if any([cell.matches_xy(c) for c in looked_for_cells.values()]):

                # Get the cell in question
                matched = []
                for i, scell in looked_for_cells.items():
                    if cell.matches_xy(scell):

                        @dataclass
                        class Match:
                            i: int
                            cell: Cell

                        matched.append(Match(i, scell))

                if len(matched) == 1:
                    row += td_selected.format(
                        value=matched[0].cell.value, colour=palette[matched[0].i]
                    )

                if len(matched) > 1:
                    row += td_selected.format(
                        value=matched[0].cell.value, colour=warning_colour
                    )
                    if not warning_used:
                        key_rows += key_row.format(
                            colour=warning_colour,
                            value="Warning: cell appears in multiple selections",
                        )
                        warning_used = True

                if len(matched) > 0:
                    for match in matched:
                        try:
                            looked_for_cells[match.i] = get_next_selected_cell(match.i)
                        except IndexError:
                            # Don't pop an empty list, eventually we exhaust all selections
                            ...
            else:
                if boundary.contains(cell):
                    row += td_unselected.format(value=cell.value)

        rows.append(tr.format(row=row))

        # Get table name
        try:
            table_name = selections[0].selected_table.name
        except UnnamedTableError:
            table_name = "unnamed table"

        if not boundary.is_pristine:
            preview_title = f"Selections made within table: {table_name}"
        else:
            preview_title = f"Pristine (no selections made) view of table: {table_name}"

        return doc.format(
            title=preview_title,
            key_rows=key_rows,
            style=inline_css,
            table=table.format(rows=f"\n".join(rows)),
        )

    def print(
        self,
        selections: List[Selectable],
        path: Path = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """
        An inline print of whatever this preview is previewing
        """
        html_as_str = self._make_preview_as_html_str(selections, start=start, end=end)
        if path:
            self._to_path(path, html_as_str)
        else:
            display(HTML(html_as_str))

    def _to_path(self, path: Path, html_as_str: str):
        """
        The mechanism to push whatever this is previewing to
        a filepath.
        """
        with open(path, "w") as f:
            f.write(html_as_str)
