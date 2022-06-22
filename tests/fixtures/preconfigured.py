
import pytest

from pivoter.exceptions import UnnamedTableError
from pivoter.models.source.table import LiveTable
from pivoter.readers.reader import read_local
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import path_to_fixture


def fixture_simple_one_tab():
    """
    Simple input of one tab. Cells A1:Z100
    """
    return read_local(
        path_to_fixture("csv", "simple.csv"), override_selectable=XlsInputSelectable
    )

def fixture_with_blanks():
    return read_local(path_to_fixture("csv", "has_blanks.csv"))


# TODO - use excel when we have a real excel reader
def fixture_simple_two_tabs():
    """
    Simple input of two tabs. Cells A1:Z100

    For test purposes we're going to load each table distinctly
    (to unsycronise their signatures) and give each distinct name
    """
    selectable1 = read_local(
        path_to_fixture("csv", "simple.csv"), override_selectable=XlsInputSelectable
    )
    table1 = LiveTable.from_table(
        selectable1.selected_table.pristine, name="I am table 1"
    )

    selectable2 = read_local(
    path_to_fixture("csv", "simple.csv"), override_selectable=XlsInputSelectable
    )
    table2 = LiveTable.from_table(
        selectable2.selected_table.pristine, name="I am table 2"
    )

    return XlsInputSelectable(
        is_singleton_table=False, selected_table=table1, tables=[table1, table2]
    )