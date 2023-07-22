import pytest

from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_assert_one(selectable_simple1: Selectable):
    """
    Test assert one behaves correctly
    """

    s = selectable_simple1.excel_ref("F93")
    s.assert_one()

    with pytest.raises(AssertionError):
        s = selectable_simple1.excel_ref("F93:G94")
        s.assert_one()

def test_assert_len(selectable_simple1: Selectable):
    """
    Test assert len behaves correctly
    """

    s = selectable_simple1.excel_ref("F93:G93")
    s.assert_len(2)

    with pytest.raises(AssertionError):
        s = selectable_simple1.excel_ref("F93:G94")
        s.assert_len(90)


def test_assert_row(selectable_simple1: Selectable):
    """
    Test assert row behaves correctly
    """

    s = selectable_simple1.excel_ref("F93:H93")
    s.assert_single_row()

    with pytest.raises(AssertionError):
        s = selectable_simple1.excel_ref("F93:G94")
        s.assert_single_row()


def test_assert_column(selectable_simple1: Selectable):
    """
    Test assert column behaves correctly
    """

    s = selectable_simple1.excel_ref("F20:F90")
    s.assert_single_column()

    with pytest.raises(AssertionError):
        s = selectable_simple1.excel_ref("F93:G94")
        s.assert_single_column()
