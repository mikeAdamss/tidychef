import pytest

from datachef import datafuncs as dfc
from datachef.direction.directions import down, left, right, up
from datachef.exceptions import AmbiguousWaffleError
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_waffle(selectable_simple1: Selectable):
    """
    Test that the expected exceptions are raised where
    the users is trying to waffle invalid selections
    """

    # Waffle right works
    selection1 = selectable_simple1.excel_ref("A2:A9")
    selection2 = selectable_simple1.excel_ref("B1:D1")
    test1 = selection1.waffle(right, selection2)
    test1.assert_len(24)
    assert dfc.basecells_to_excel_ref(test1.cells) == "B2:D9"

    # Waffle right fails for overlap
    with pytest.raises(AmbiguousWaffleError):
        selection1 = selectable_simple1.excel_ref("A2:A9")
        selection2 = selectable_simple1.excel_ref("A1:D1")
        selection1.waffle(right, selection2)

    # Waffle up
    selection1 = selectable_simple1.excel_ref("D2:F2")
    selection2 = selectable_simple1.excel_ref("A1")
    test2 = selection1.waffle(up, selection2)
    test2.assert_len(3)
    assert dfc.basecells_to_excel_ref(test2.cells) == "D1:F1"

    # Waffle up fails for overlap
    with pytest.raises(AmbiguousWaffleError):
        selection1 = selectable_simple1.excel_ref("D2:F2")
        selection2 = selectable_simple1.excel_ref("A2")
        selection1.waffle(up, selection2)

    # Waffle left works
    selection1 = selectable_simple1.excel_ref("G2:G9")
    selection2 = selectable_simple1.excel_ref("B1:D1")
    test3 = selection1.waffle(left, selection2)
    test3.assert_len(24)
    assert dfc.basecells_to_excel_ref(test3.cells) == "B2:D9"

    # Waffle left fails for overlap
    with pytest.raises(AmbiguousWaffleError):
        selection1 = selectable_simple1.excel_ref("G2:G9")
        selection2 = selectable_simple1.excel_ref("D1:G1")
        selection1.waffle(left, selection2)

    # Waffle down works
    selection1 = selectable_simple1.excel_ref("D1:G1")
    selection2 = selectable_simple1.excel_ref("G2:G9")
    test4 = selection1.waffle(down, selection2)
    test4.assert_len(32)
    assert dfc.basecells_to_excel_ref(test4.cells) == "D2:G9"

    # Waffle down fails for overlap
    with pytest.raises(AmbiguousWaffleError):
        selection1 = selectable_simple1.excel_ref("D1:G2")
        selection2 = selectable_simple1.excel_ref("G1:G9")
        selection1.waffle(down, selection2)
