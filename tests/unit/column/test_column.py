import pytest

from datachef.column.column import Column
from datachef.lookup.engines.constant import Constant
from datachef.models.source.cell import VirtualCell


def test_resolving_column_value_from_observation():
    """
    Test the basic resolver can be called as expected
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = Column("This", Constant("foo"))
    assert col.resolve_column_value_from_obs(ob_cell).value == "foo"


def test_apply_can_be_passed_in_short_and_long_form():
    """
    Test that a user can pass in a callable via
    either apply= or a=
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = Column("This", Constant("foo"), apply=lambda x: x + "-bar")
    assert col.resolve_column_value_from_obs(ob_cell).value == "foo-bar"

    col = Column("This", Constant("foo"), a=lambda x: x + "-baz")
    assert col.resolve_column_value_from_obs(ob_cell).value == "foo-baz"
