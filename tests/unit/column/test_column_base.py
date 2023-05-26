import pytest

from datachef.column.base import BaseColumn
from datachef.lookup.engines.constant import Constant
from datachef.models.source.cell import VirtualCell
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def all_cells_from_a_tab():
    return fixture_simple_one_tab()


def test_resolving_base_column_value_from_observation():
    """
    Test the basic resolver can be called as expected
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = BaseColumn("This", Constant("foo"))
    assert col.resolve_column_value_from_obs(ob_cell).value == "foo"


def test_base_column_assertions():
    """
    Test that the assertions trigger as expected.

    Note, given that we're not doing the lookup
    we'll just use a Constant lookup engine.
    """

    # Incorrect type for label
    with pytest.raises(AssertionError):
        BaseColumn(
            True,
            Constant("foo"),
        )

    # Incorrect type for lookup engine
    with pytest.raises(AssertionError):
        BaseColumn(
            "I r a label",
            True,
        )

    # Does not raise for correct arguments
    BaseColumn("I r a label", Constant("foo"))


def test_base_column_pre_init():
    ...
