"""
Tests relating to pivoters underlying pivoter.models.source.BaseInput class
and its use in a users workflow
"""

import pytest

from datachef.exceptions import IteratingSingleTableError, UnnamedTableError
from datachef.selection.selectable import Selectable
from tests.fixtures.preconfigured import fixture_simple_one_tab, fixture_simple_two_tabs


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


@pytest.fixture
def selectable_of2_simple1():
    return fixture_simple_two_tabs()


def test_cannot_iterate_single_table_inputs(selectable_simple1: Selectable):
    """
    Confirm the appropriate error is raised where a user tries to
    iterate through an input consisting of exactly one table.
    """

    with pytest.raises(IteratingSingleTableError):
        for table in selectable_simple1:
            """never triggered"""


def test_selectable_name_property_returns_name(selectable_of2_simple1: Selectable):
    """
    If a table is named, confirm we can access the name
    property.
    """
    assert selectable_of2_simple1.name == "I am table 1"


def test_can_iterate_multiple_table_inputs(selectable_of2_simple1: Selectable):
    """
    Confirm the user can iterate through the tables in the expected
    manner.
    """

    for i, table in enumerate(selectable_of2_simple1):
        if i == 0:
            assert table.name == "I am table 1"
        if i == 1:
            assert table.name == "I am table 2"
        assert i == 0 or i == 1


# Note: title as an alternate property acvessor for name is included
# for backwards compatibiity with the databaker library
def test_input_title_property_returns_name(selectable_of2_simple1: Selectable):
    """
    If a table is named, confirm we can access the name
    via the alt property title.
    """
    assert selectable_of2_simple1.title == "I am table 1"


def test_input_name_property_unset_raises_err(selectable_simple1: Selectable):
    """
    If a table is not named, confirm accessing its name
    property returns the appropriate error.
    """

    with pytest.raises(UnnamedTableError):
        selectable_simple1.name
