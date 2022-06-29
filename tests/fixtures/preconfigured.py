import pytest

from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from datachef.models.source.table import LiveTable, Table
from datachef.readers.reader import read_local
from datachef.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import path_to_fixture


def fixture_simple_one_tab():
    """Simple input of one tab. Cells A1:Z100"""
    return read_local(
        path_to_fixture("csv", "simple.csv"), override_selectable=XlsInputSelectable
    )


def fixture_simple_small_one_tab():
    """Simple input of one tab. Cells A1:K20"""
    return read_local(
        path_to_fixture("csv", "simple-small.csv"),
        override_selectable=XlsInputSelectable,
    )


def fixture_with_blanks():
    return read_local(path_to_fixture("csv", "has_blanks.csv"))


def fixture_is_wide():
    return read_local(
        path_to_fixture("csv", "wide.csv"), override_selectable=XlsInputSelectable
    )


# TODO - use excel when we have a real excel reader
def fixture_simple_two_tabs():
    """Simple input of two tabs. Cells A1:Z100"""
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
