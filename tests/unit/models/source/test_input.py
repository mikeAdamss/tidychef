"""
Tests relating to pivoters underlying pivoter.models.source.BaseInput class
and its use in a users workflow
"""

import pytest

from pivoter.exceptions import IteratingSingleTableError, UnnamedTableError
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures.preconfigured import (fixture_simple_one_tab,
                                          fixture_simple_two_tabs)


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


@pytest.fixture
def sheet_of_two_tables():
    return fixture_simple_two_tabs()


def test_cannot_iterate_single_table_inputs(table_simple_as_xls1: XlsInputSelectable):
    """
    Confirm the appropriate error is raised where a user tries to
    iterate through an input consisting of exactly one table.
    """

    with pytest.raises(IteratingSingleTableError):
        for table in table_simple_as_xls1:
            """never triggered"""


def test_selectable_name_property_returns_name(sheet_of_two_tables: XlsInputSelectable):
    """
    If a table is named, confirm we can access the name
    property.
    """
    assert sheet_of_two_tables.name == "I am table 1"


def test_can_iterate_multiple_table_inputs(sheet_of_two_tables: XlsInputSelectable):
    """
    Confirm the user can iterate through the tables in the expected
    manner.
    """

    for i, table in enumerate(sheet_of_two_tables):
        if i == 0:
            assert table.name == "I am table 1"
        if i == 1:
            assert table.name == "I am table 2"
        assert i == 0 or i == 1


# Note: title as an alternate property acvessor for name is included
# for backwards compatibiity with the databaker library
def test_input_title_property_returns_name(sheet_of_two_tables: XlsInputSelectable):
    """
    If a table is named, confirm we can access the name
    via the alt property title.
    """
    assert sheet_of_two_tables.title == "I am table 1"


def test_input_name_property_unset_raises_err(table_simple_as_xls1: XlsInputSelectable):
    """
    If a table is not named, confirm accessing its name
    property returns the appropriate error.
    """

    with pytest.raises(UnnamedTableError):
        table_simple_as_xls1.name
