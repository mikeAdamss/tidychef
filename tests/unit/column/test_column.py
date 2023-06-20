import pytest

from datachef.column.column import Column
from datachef.lookup.engines.constant import Constant
from datachef.models.source.cell import VirtualCell


def test_resolving_column_value_from_observation():
    """
    Test the basic resolver can be called as expected
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = Column(Constant("This", "foo"))
    assert col.resolve_column_cell_from_obs_cell(ob_cell).value == "foo"


def test_apply_can_be_specified():
    """
    Test that apply= works as expected
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = Column(Constant("This", "foo"), apply=lambda x: x + "-bar")
    assert col.resolve_column_cell_from_obs_cell(ob_cell).value == "foo-bar"

def test_validation_can_be_specified():
    """
    Test that validation= works as expected
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = Column(Constant("This", "foo"), validation=lambda x: x)
    assert col.resolve_column_cell_from_obs_cell(ob_cell).value == "foo"
