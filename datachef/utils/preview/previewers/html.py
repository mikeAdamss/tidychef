"""
TODO - works but messy, rewrite for clarity once we've a comprehensive test
suite in place.
"""

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Union

from dominate.tags import *
from IPython.display import HTML, display

from datachef.exceptions import UnnamedTableError
from datachef.models.source.cell import BaseCell, Cell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable
from datachef.utils import cellutils

from ..base import BasePreview


class HtmlPreview(BasePreview):
    """
    Class representing a html previewed selection.
    """

    def _make_preview_as_html_str(
        self,
        selections: Union[Selectable, Tuple[Selectable]],
        with_excel_ref: bool = True,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> str:

        is_pristine = not all([s.selections_made() for s in selections])

        if end == "select" and is_pristine:
            raise Exception(
                "You cannot bound the preview to only show up to selections when you haven't made any selections!"
            )

        # Where we have a boundary, first assume its the default - to the bottomright most selected cell
        if end:
            max_selected_x = max(dfc.maximum_x_offset(s.cells) for s in selections)
            max_selected_y = max(dfc.maximum_y_offset(s.cells) for s in selections)

        if start:
            min_selected_x = max(dfc.minimum_x_offset(s.cells) for s in selections)
            min_selected_y = max(dfc.minimum_y_offset(s.cells) for s in selections)

        # Allow the user to specify the bottomright most cell to preview until, but only where this
        # would not obscure cell selections
        if end and end != "selection":
            boundary_cell: BaseCell = dfc.single_excel_ref_to_basecell(end)
            assert (
                boundary_cell.x >= max_selected_x
            ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a column limit of {cellutils.x_to_letters(boundary_cell.x)} but have an x axis selection in column {cellutils.x_to_letters(max_selected_x)}"
            assert (
                boundary_cell.y >= max_selected_y
            ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a row limit of {cellutils.y_to_number(boundary_cell.y)} but have an y axis selection on row {cellutils.y_to_number(max_selected_y)}"
            max_selected_x = boundary_cell.x
            max_selected_y = boundary_cell.y

        # Allow the user to specify the topleft most cell to start tne preview, but only where this
        # would not obscure cell selections
        if start and start != "selection":
            boundary_cell: BaseCell = dfc.single_excel_ref_to_basecell(start)
            assert (
                boundary_cell.x <= max_selected_x
            ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a column limit of {cellutils.x_to_letters(boundary_cell.x)} but have an x axis selection in column {cellutils.x_to_letters(max_selected_x)}"
            assert (
                boundary_cell.y <= max_selected_y
            ), f"You cannot set preview to ignore selected cells. With a boundary point of {end}, you have a row limit of {cellutils.y_to_number(boundary_cell.y)} but have an y axis selection on row {cellutils.y_to_number(max_selected_y)}"
            min_selected_x = boundary_cell.x
            min_selected_y = boundary_cell.y

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

        all_cells: List[Cell] = dfc.ensure_human_read_order(selections[0].pcells)

        key_rows = ""
        selected_cells_index = {}
        for i, s in enumerate(selections):
            selected_cells_index[i] = deque(dfc.ensure_human_read_order(s.cells))
            key_rows += key_row.format(
                colour=palette[i], value=s._label if s._label else f"selection {i}"
            )

        def get_next_selected_cell(i: int) -> Cell:
            next_cell = selected_cells_index[i].popleft()
            return next_cell

        looked_for_cells = {}
        for i in selected_cells_index.keys():
            looked_for_cells[i] = get_next_selected_cell(i)

        rows = []
        row = ""
        row_no = 0

        if with_excel_ref:
            # Add header row
            row += td_unselected.format(value="")
            for cell in all_cells:
                if cell.y == row_no:
                    if end:
                        if cell.x > max_selected_x:
                            continue
                    if start:
                        if cell.x < min_selected_x:
                            continue
                    row += td_unselected.format(value=cellutils.x_to_letters(cell.x))
                else:
                    rows.append(tr.format(row=row))
                    row = ""

                    # If we havnt designated a start y position for the preview
                    # or if the desiganted start y == 0,
                    # then add the row heading letter
                    if not start:
                        row += td_unselected.format(value=cell.y)
                    elif min_selected_y == 0:
                        row += td_unselected.format(value=cell.y)
                    break

        for cell in all_cells:
            if cell.y != row_no:
                if end:
                    if cell.y > max_selected_y:
                        break
                row_no += 1
                rows.append(tr.format(row=row))
                row = ""
                if with_excel_ref:
                    if start:
                        if cell.y < min_selected_y:
                            continue
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
                            ...
            else:
                if end:
                    if cell.x > max_selected_x:
                        continue
                if start:
                    if cell.y < min_selected_y:
                        continue
                    if cell.x < min_selected_x:
                        continue

                row += td_unselected.format(value=cell.value)

        rows.append(tr.format(row=row))

        # Get table name
        try:
            table_name = selections[0].name
        except UnnamedTableError:
            table_name = "unnamed table"

        if not is_pristine:
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
