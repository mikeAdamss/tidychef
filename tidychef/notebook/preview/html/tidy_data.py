from typing import List

from .components import HtmlCell
from .constants import BORDER_CELL_COLOUR, INLINE_CSS, NO_COLOUR


def tidy_data_as_html_table_string(data: List[List[str]]) -> str:
    """
    When given tidy data in the form of a list of lists,i.e

    [
        ["row 1 value 1", "row 1 value 2"],
        ["row 2 value 1", "row 2 value 2"],
        etc...
    ]

    Return a html table representation of same.
    """

    headers = data[0]
    table_html = f"<tr>{''.join([HtmlCell(x, BORDER_CELL_COLOUR).as_html() for x in headers])}</tr>"

    rows = data[1:]
    for row in rows:
        table_html += (
            f"<tr>{''.join([HtmlCell(x, NO_COLOUR).as_html() for x in row])}</tr>"
        )

    return f"""
    <html>
        {INLINE_CSS}
            <body>
                <table>
                    {table_html}
                </table>
            </body>
            <br>
        </html>
    """
