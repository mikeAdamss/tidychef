import pytest

from datachef.exceptions import (
    BadExcelReferenceError,
    LoneValueOnMultipleCellsError,
    ReferenceOutsideSelectionError,
)
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_lone_value_selector(selectable_simple1: Selectable):
    """
    Test we can return the value for selections of exactly one cell
    """
    assert selectable_simple1.excel_ref("A1").lone_value() == "A1val"


def test_lone_value_on_multiple_values_errors(
    selectable_simple1: Selectable,
):
    """
    Test than calling Input.lone_value() on a filtered table containing
    more than one value raises.
    """

    with pytest.raises(LoneValueOnMultipleCellsError):
        selectable_simple1.excel_ref("A1:A2").lone_value()


def test_excel_referece_does_not_error(
    selectable_simple1: Selectable,
):
    """
    Test that we cannot select using an excel reference for cells that
    don't exist in either the current selection or the pristine selection
    """

    # Single cell
    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("AA2")

    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("B2").excel_ref("A2")

    # Range of cells
    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("B9:ZZZ2930")

    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("A1:B2").excel_ref("F1:G2")

    # Single column
    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("ZZZZ")

    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("A").excel_ref("B")

    # Range of columns
    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("A:ZZZZZ")

    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("A:B").excel_ref("C:D")

    # Single row
    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("98928")

    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("2").excel_ref("3")

    # Range of rows
    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("9:2930")

    with pytest.raises(ReferenceOutsideSelectionError):
        selectable_simple1.excel_ref("1:3").excel_ref("2:4")


def test_excel_reference_bad_reference_error(
    selectable_simple1: Selectable,
):
    """
    Test that we cannot select using an excel reference for cells that
    are not within the current selection
    """

    with pytest.raises(BadExcelReferenceError):
        selectable_simple1.excel_ref("*nope")

    with pytest.raises(BadExcelReferenceError):
        selectable_simple1.excel_ref("8:4")

    with pytest.raises(BadExcelReferenceError):
        selectable_simple1.excel_ref("D:A")


def test_list_excel_refs(selectable_simple1: Selectable):
    """
    Test that the user can list their cells as
    a list of simple excel references if need be.
    """

    selection = selectable_simple1.excel_ref("B6:E7") - selectable_simple1.excel_ref(
        "D7"
    )
    assert selection._get_excel_references() == [
        "B6",
        "C6",
        "D6",
        "E6",
        "B7",
        "C7",
        "E7",
    ]
