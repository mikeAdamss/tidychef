import pytest

from datachef.column.base import BaseColumn
from datachef.lookup.engines.constant import Constant
from datachef.models.source.cell import VirtualCell
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def all_cells_from_a_tab() -> Selectable:
    return fixture_simple_one_tab()


def test_resolving_base_column_value_from_observation():
    """
    Test the basic resolver can be called as expected
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = BaseColumn(Constant("This", "foo"))
    assert col.resolve_column_cell_from_obs_cell(ob_cell).value == "foo"


def test_base_column_assertions():
    """
    Test that the assertions trigger as expected.

    Note, given that we're not doing the lookup
    we'll just use a Constant lookup engine.
    """

    # Incorrect type for lookup engine
    with pytest.raises(AssertionError):
        BaseColumn(
            True,
        )

    # Does not raise for incorrect arguments
    BaseColumn(Constant("I r a label", "foo"))
