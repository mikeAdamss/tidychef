import pytest

from pivoter.cardinal.directions import DOWN, LEFT, RIGHT, UP
from pivoter.exceptions import BadShiftParameterError, OutOfBoundsError
from pivoter.selection import datafuncs as dfc
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


def test_shift(table_simple_as_xls1: XlsInputSelectable):
    """
    Test we can shift in the LEFT and RIGHT cardinal direction.
    """

    s = table_simple_as_xls1.excel_ref("B3:D4")
    assert len(s.cells) == 6
    s = s.shift(RIGHT)
    assert dfc.xycells_to_excel_ref(s.cells) == "C3:E4"
    assert len(s.cells) == 6

    s = table_simple_as_xls1.excel_ref("B3:D4")
    assert len(s.cells) == 6
    s = s.shift(RIGHT(1))
    assert dfc.xycells_to_excel_ref(s.cells) == "C3:E4"
    assert len(s.cells) == 6

    s = table_simple_as_xls1.excel_ref("B3:D4")
    assert len(s.cells) == 6
    s = s.shift(RIGHT(3))
    assert dfc.xycells_to_excel_ref(s.cells) == "E3:G4"
    assert len(s.cells) == 6

    s = table_simple_as_xls1.excel_ref("B3:D4")
    assert len(s.cells) == 6
    s = s.shift(RIGHT(3)).shift(DOWN(7))
    assert dfc.xycells_to_excel_ref(s.cells) == "E10:G11"
    assert len(s.cells) == 6

    s = table_simple_as_xls1.excel_ref("F10:H21")
    assert len(s.cells) == 36
    s = s.shift(LEFT(2)).shift(UP(6))
    assert dfc.xycells_to_excel_ref(s.cells) == "D4:F15"
    assert len(s.cells) == 36

    s = table_simple_as_xls1.excel_ref("L12:M14")
    assert len(s.cells) == 6
    s = s.shift(3, 3)
    assert dfc.xycells_to_excel_ref(s.cells) == "O15:P17"
    assert len(s.cells) == 6

    s = table_simple_as_xls1.excel_ref("L12:M14")
    assert len(s.cells) == 6
    s = s.shift(3, -3)
    assert dfc.xycells_to_excel_ref(s.cells) == "O9:P11"
    assert len(s.cells) == 6


def test_bad_shift_parameters(table_simple_as_xls1: XlsInputSelectable):
    """
    Confirm that intorrect shift parameters passed into shift
    raise the appropriate error.
    """
    for params in [[1, "foo"], [object, 12], [None, 4]]:

        with pytest.raises(BadShiftParameterError):
            table_simple_as_xls1.shift(params[0], params[1])


def test_shift_out_of_bounds_raises(table_simple_as_xls1: XlsInputSelectable):
    """
    Make sure an appropriate error is raised if we try and shift
    outisde the boundaries of the initial provided table of data.
    """

    with pytest.raises(OutOfBoundsError):
        table_simple_as_xls1.excel_ref("Z100").shift(RIGHT)
