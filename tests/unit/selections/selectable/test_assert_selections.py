import pytest

from datachef.exceptions import IncorrectAssertionError
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_assert_selections_errors_for_bad_constructor(selectable_simple1: Selectable):
    """
    Test that the correct error is raised where a user incorrectly
    configures the .assert_selections() method.
    """

    # Should error for more than one kwarg
    with pytest.raises(IncorrectAssertionError):
        selectable_simple1.assert_selections(are_one_of=[], match="")

    # Should error for 0 kwargs
    with pytest.raises(IncorrectAssertionError):
        selectable_simple1.assert_selections()


def test_assert_selections_are_one_of(selectable_simple1: Selectable):
    """
    Test that the are_of_of= kwarg for assert_selections works
    as expected.
    """

    a_cells = selectable_simple1.excel_ref("A1:A4")

    # Should not raise an AssertionError
    a_cells.assert_selections(are_one_of=["A1val", "A2val", "A3val", "A4val"])

    # Should raise an exception
    with pytest.raises(AssertionError):
        a_cells.assert_selections(are_one_of=["A1val"])


def test_assert_selections_match(selectable_simple1: Selectable):
    """
    Test that the match= kwarg for assert_selections works
    as expected.
    """

    a_cells = selectable_simple1.excel_ref("A1:A4")

    # Should not raise an AssertionError
    a_cells.assert_selections(match="A[1-4]val")

    # Should raise an exception
    with pytest.raises(AssertionError):
        a_cells.assert_selections(match="foo")


def test_assert_selections_using(selectable_simple1: Selectable):
    """
    Test that the sing= kwarg for assert_selections works
    as expected.
    """

    def a_asserter(cell: Cell):
        assert cell.value in ["A1val", "A2val", "A3val", "A4val"]

    a_cells = selectable_simple1.excel_ref("A1:A4")

    # Should not raise an AssertionError
    a_cells.assert_selections(using=a_asserter)

    # Should raise an exception
    with pytest.raises(AssertionError):
        a_cells = selectable_simple1.excel_ref("A1:A5")
        a_cells.assert_selections(match="foo")
