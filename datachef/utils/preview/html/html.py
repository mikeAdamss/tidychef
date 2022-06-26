from collections import deque
from pathlib import Path
from typing import List

from dominate.tags import *
from IPython.display import HTML, display

from datachef.exceptions import UnnamedTableError
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.utils import cellutils

from ..base import BasePreview


class HtmlPreview(BasePreview):
    """
    Class representing a html previewed selection.
    """

    def _make_preview_as_html_str(
        self, with_excel_ref: bool = True, bound_selection=False
    ) -> str:

        is_pristine = not self.selectable.selections_made()
        if bound_selection and is_pristine:
            raise Exception(
                "You cannot bound the selection (only show relevent selections) when you haven't made any selections!"
            )

        if bound_selection:
            max_selected_x = dfc.maximum_x_offset(self.selectable.cells)
            max_selected_y = dfc.maximum_y_offset(self.selectable.cells)

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
            <body>
                <h2>{title}</h2>
                {table}
            </body>
        </html>
        """

        table = """
            <table>
                {rows}
            </table>
        """

        tr = "<tr>{row}</tr>"

        td_unselected = "<td>{value}</td>"
        td_selected = '<td style="background-color:cyan">{value}</td>'

        all_cells: List[Cell] = dfc.ensure_human_read_order(self.selectable.pcells)
        selected_cells = deque(dfc.ensure_human_read_order(self.selectable.cells))

        def get_next_selected_cell() -> Cell:
            s = selected_cells.popleft()
            return s

        next_selected_cell = get_next_selected_cell()

        rows = []
        row = ""
        row_no = 0

        if with_excel_ref:
            # Add header row
            row += td_unselected.format(value="")
            for cell in all_cells:
                if cell.y == row_no:
                    if bound_selection:
                        if cell.x > max_selected_x:
                            continue
                    row += td_unselected.format(value=cellutils.x_to_letters(cell.x))
                else:
                    rows.append(tr.format(row=row))
                    row = ""
                    row += td_unselected.format(value=cell.y)
                    break

        for cell in all_cells:
            if cell.y != row_no:
                if bound_selection:
                    if cell.y > max_selected_y:
                        break
                row_no += 1
                rows.append(tr.format(row=row))
                row = ""
                if with_excel_ref:
                    row += td_unselected.format(value=cell.y + 1)

            if cell.matches_xy(next_selected_cell):
                try:
                    row += td_selected.format(value=next_selected_cell.value)
                    try:
                        next_selected_cell = get_next_selected_cell()
                    except IndexError:
                        ...
                except KeyError:
                    raise Exception(next_selected_cell)
            else:
                if bound_selection:
                    if cell.x > max_selected_x:
                        continue
                row += td_unselected.format(value=cell.value)

        rows.append(tr.format(row=row))

        # Get table name
        try:
            table_name = self.selectable.name
        except UnnamedTableError:
            table_name = "unnamed table"

        if is_pristine:
            preview_title = f"Selections made within table: {table_name}"
        else:
            preview_title = f"Pristine (no selections made) view of table: {table_name}"

        return doc.format(
            title=preview_title,
            style=inline_css,
            table=table.format(rows=f"\n".join(rows)),
        )

    def print(self, path: Path = None, bound_selection: bool = False):
        """
        An inline print of whatever this preview is previewing
        """
        if path:
            self._to_path(path)
        html_as_str = self._make_preview_as_html_str(bound_selection=bound_selection)
        display(HTML(html_as_str))

    def _to_path(self, path: Path):
        """
        The mechanism to push whatever this is previewing to
        a filepath.
        """
        with open(path, "w") as f:
            f.write(self._make_preview_as_html_str())
