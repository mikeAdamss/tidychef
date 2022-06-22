"""
Tests relating to pivoters underlying pivoter.models.source.BaseInput class
and its use in a users workflow
"""

import pytest

from pivoter.exceptions import IteratingSingleTableError
from pivoter.selection.spreadsheet.xls import XlsInputSelectable

from pivoter.readers.reader import read_local
from tests.fixtures import path_to_fixture


@pytest.fixture
def table_simple_as_xls1():
    return read_local(
        path_to_fixture("csv", "simple.csv"),
        override_selectable = XlsInputSelectable
    )


def test_cannot_iterate_single_table_inputs(table_simple_as_xls1: XlsInputSelectable):
    """
    Confirm the appropriate error is raised where a user tries to
    iterate through an input consisting of exactly one table.
    """

    with pytest.raises(IteratingSingleTableError):
        for table in table_simple_as_xls1:
            """never triggered"""


# def test_can_iterate_multiple_table_inputs(multiple_input_A1: BaseInput):
#     """
#     Confirm the user can iterate through the tables in the expected
#     manner.
#     """

#     for i, table in enumerate(multiple_input_A1):
#         if i == 0:
#             assert table.name == "single input A1 table 1"
#         if i == 1:
#             assert table.name == "single input A1 table 2"
#         assert i == 0 or i == 1


# def test_table_name_property_returns_name(single_input_A1: BaseInput):
#     """
#     If a table is named, confirm we can access the name
#     property.
#     """
#     assert single_input_A1.name == "single input A1"


# # Note: title as an alternate property acvessor for name is included
# # for backwards compatibiity with the databaker library
# def test_table_title_property_returns_name(single_input_A1: BaseInput):
#     """
#     If a table is named, confirm we can access the name
#     via the alt property title.
#     """
#     assert single_input_A1.title == "single input A1"


# def test_table_name_property_raises_err(single_unnamed_input_A1: BaseInput):
#     """
#     If a table is not named, confirm accessing its name
#     property returns the appropriate error.
#     """

#     with pytest.raises(UnnamedTableError):
#         single_unnamed_input_A1.name
