from datachef.models.source.input import BaseInput
from datachef.models.source.table import LiveTable, Table
from datachef.readers.reader import read_local
from datachef.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import path_to_fixture


def fixture_simple_band_tab():
    """Slim version of a our sample band data"""
    return read_local(
        path_to_fixture("csv", "bands.csv"), override_selectable=XlsInputSelectable
    )


def fixture_wide_band_tab():
    """Wide version of our sample band data"""
    return read_local(
        path_to_fixture("csv", "bands-wide.csv"), override_selectable=XlsInputSelectable
    )


def fixture_vertical_dimensions():
    """Wide version of our sample band data"""
    return read_local(
        path_to_fixture("csv", "vertical-dimensions.csv"),
        override_selectable=XlsInputSelectable,
    )


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

    test_input_path = path_to_fixture("csv", "simple.csv")
    selectable1 = read_local(
        test_input_path, override_selectable=XlsInputSelectable
    )
    table1 = LiveTable.from_table(
        selectable1.pristine, name="I am table 1", source=test_input_path
    )

    selectable2 = read_local(
        test_input_path, override_selectable=XlsInputSelectable
    )
    table2 = LiveTable.from_table(
        selectable2.pristine, name="I am table 2", source=test_input_path
    )

    return BaseInput(
        had_initial_path=test_input_path,
        tables=[table1, table2]
    )
