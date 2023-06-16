from datachef.models.source.input import BaseInput
from datachef.models.source.table import LiveTable, Table
from datachef import acquire
from datachef.selection.selectable import Selectable
from tests.fixtures import path_to_fixture


def fixture_simple_band_tab():
    """
    Slim version of a our sample band data

    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/bands.csv

    local:
    datachef/tests/fixtures/csv/bands.csv
    """
    return acquire.csv.local(
        path_to_fixture("csv", "bands.csv")
    )


def fixture_wide_band_tab():
    """
    Wide version of our sample band data

    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/bands-wide.csv

    local:
    datachef/tests/fixtures/csv/bands-wide.csv
    """
    return acquire.csv.local(
        path_to_fixture("csv", "bands-wide.csv"))


def fixture_vertical_dimensions():
    """Wide version of our sample band data"""
    return acquire.csv.local(
        path_to_fixture("csv", "vertical-dimensions.csv")
    )


def fixture_simple_one_tab():
    """
    Simple input of one tab. Cells A1:Z100
    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/simple.csv

    local:
    datachef/tests/fixtures/csv/simple.csv
    """
    return acquire.csv.local(
        path_to_fixture("csv", "simple.csv")
    )


def fixture_simple_small_one_tab():
    """
    Simple input of one tab. Cells A1:K20
    
    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/simple-small.csv

    local:
    datachef/tests/fixtures/csv/simple-small.csv
    """
    return acquire.csv.local(
        path_to_fixture("csv", "simple-small.csv")
    )


def fixture_with_blanks():
    """
    Simple data with blanks in it

    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/has_blanks.csv

    local:
    datachef/tests/fixtures/csv/has_blanks.csv
    """
    return acquire.csv.local(path_to_fixture("csv", "has_blanks.csv"))


def fixture_is_wide():
    """
    Wide version of simple data

    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/wide.csv

    local:
    datachef/tests/fixtures/csv/wide.csv
    """
    return acquire.csv.local(
        path_to_fixture("csv", "wide.csv")
    )


# TODO - use excel when we have a real excel reader
def fixture_simple_two_tabs():
    """Simple input of two tabs. Cells A1:Z100"""

    test_input_path = path_to_fixture("csv", "simple.csv")
    selectable1: Selectable = acquire.csv.local(test_input_path)
    table1 = LiveTable.from_table(
        selectable1.pristine, name="I am table 1", source=test_input_path
    )

    selectable2: Selectable = acquire.csv.local(test_input_path)
    table2 = LiveTable.from_table(
        selectable2.pristine, name="I am table 2", source=test_input_path
    )

    return BaseInput(had_initial_path=test_input_path, tables=[table1, table2])
