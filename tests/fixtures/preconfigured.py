from tidychef import acquire
from tests.fixtures import path_to_fixture


def fixture_simple_band_tab():
    """
    Slim version of a our sample band data

    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/bands.csv

    local:
    datachef/tests/fixtures/csv/bands.csv
    """
    return acquire.csv.local(path_to_fixture("csv", "bands.csv"))


def fixture_wide_band_tab():
    """
    Wide version of our sample band data

    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/bands-wide.csv

    local:
    datachef/tests/fixtures/csv/bands-wide.csv
    """
    return acquire.csv.local(path_to_fixture("csv", "bands-wide.csv"))


def fixture_vertical_dimensions():
    """Wide version of our sample band data"""
    return acquire.csv.local(path_to_fixture("csv", "vertical-dimensions.csv"))


def fixture_simple_one_tab():
    """
    Simple input of one tab. Cells A1:Z100
    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/simple.csv

    local:
    datachef/tests/fixtures/csv/simple.csv
    """
    return acquire.csv.local(path_to_fixture("csv", "simple.csv"))


def fixture_simple_small_one_tab():
    """
    Simple input of one tab. Cells A1:K20

    remote:
    https://github.com/mikeAdamss/datachef/blob/main/tests/fixtures/csv/simple-small.csv

    local:
    datachef/tests/fixtures/csv/simple-small.csv
    """
    return acquire.csv.local(path_to_fixture("csv", "simple-small.csv"))


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
    return acquire.csv.local(path_to_fixture("csv", "wide.csv"))
