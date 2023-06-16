import pytest

from datachef import acquire
from datachef.column.base import BaseColumn
from datachef.selection.selectable import Selectable
from datachef.lookup.engines.constant import Constant
from datachef.models.source.cell import VirtualCell
from tests.fixtures import fixture_simple_one_tab, path_to_fixture


@pytest.fixture
def all_cells_from_a_tab() -> Selectable:
    return fixture_simple_one_tab()


def test_resolving_base_column_value_from_observation():
    """
    Test the basic resolver can be called as expected
    """

    ob_cell = VirtualCell("value unused as we're using a constant lookup")

    col = BaseColumn("This", Constant("foo"))
    assert col.resolve_column_cell_from_obs_cell(ob_cell).value == "foo"


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

    # Does not raise for incorrect arguments
    BaseColumn("I r a label", Constant("foo"))


def test_base_column_lookup_preview(all_cells_from_a_tab: Selectable):
    """
    Test that a user can create the generator to
    preview lookups.
    """

    column = BaseColumn("I r a label", Constant("foo"))

    observations_selection = all_cells_from_a_tab.excel_ref("C7:E10")

    count = 0
    for ob_cell, looked_up_cell in column.lookup_preview(observations_selection):
        assert (
            ob_cell == observations_selection.cells[count]
            and looked_up_cell.value == "foo"
        )
        count += 1
