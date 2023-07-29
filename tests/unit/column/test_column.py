import pytest

from tidychef import acquire, against
from tidychef.column.column import Column
from tidychef.direction import down
from tidychef.exceptions import CellValidationError
from tidychef.lookup.engines.constant import Constant
from tidychef.models.source.cell import Cell
from tidychef.selection import Selectable


def test_resolving_column_value_from_observation():
    """
    Test the basic resolver can be called as expected
    """

    ob_cell = Cell(x="1", y="1", value="value unused as we're using a constant lookup")

    col = Column.constant("This", "foo")
    assert col.resolve_column_cell_from_obs_cell(ob_cell).value == "foo"


def test_apply_can_be_specified():
    """
    Test that apply= works as expected
    """

    ob_cell = Cell(x="1", y="1", value="value unused as we're using a constant lookup")

    col = Column(Constant("This", "foo"), apply=lambda x: x + "-bar")
    assert col.resolve_column_cell_from_obs_cell(ob_cell).value == "foo-bar"


def test_apply_results_are_cached_so_same_modification_is_not_resolved_multiple_times():
    """
    Test that apply= works as expected and caches the results of turning A into B
    where multiple instances of A are provided.
    """

    data: Selectable = acquire.python.list_of_lists(
        [["Male", "Male", "Female"], ["1", "2", "3"], ["4", "5", "6"]]
    ).label_as("unused but required")

    column = Column(
        data.excel_ref("1").finds_observations_directly(down), apply=lambda x: x
    )
    for ob_cell in data - data.excel_ref("1"):
        column.resolve_column_cell_from_obs_cell(ob_cell)

    # Despite having three columns headers being modified, our
    # apply cache should only have 2 values in it.
    assert len(column._apply_cache) == 2


def test_apply_results_are_unique_to_a_given_column_context():
    """
    Test that apply= works as expected and does not modify the underlying
    cell when its also used by a different column
    """

    data: Selectable = acquire.python.list_of_lists([["Male"], ["1"]]).label_as(
        "unused but required"
    )

    column1 = Column(
        data.excel_ref("1").finds_observations_directly(down),
        apply=lambda x: "foo " + x,
    )
    column2 = Column(data.excel_ref("1").finds_observations_directly(down))
    for ob_cell in data - data.excel_ref("1"):
        assert column1.resolve_column_cell_from_obs_cell(ob_cell).value == "foo Male"
        assert column2.resolve_column_cell_from_obs_cell(ob_cell).value == "Male"


def test_column_validation():
    """
    Test that validation= assugnment works as expected
    """

    ob_cell = Cell(x="1", y="1", value="value unused as we're using a constant lookup")

    col = Column(Constant("This", "foo"), validate=lambda x: x == "bar")
    with pytest.raises(CellValidationError):
        col.resolve_column_cell_from_obs_cell(ob_cell)

    col = Column(Constant("This", "foo"), validate=against.is_numeric)
    with pytest.raises(CellValidationError):
        col.resolve_column_cell_from_obs_cell(ob_cell)
