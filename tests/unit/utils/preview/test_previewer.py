import pytest

from datachef.selection.selectable import Selectable
from datachef.utils.preview.previewer import preview
from tests.fixtures.preconfigured import fixture_simple_small_one_tab


@pytest.fixture
def selectable_simple_small1():
    return fixture_simple_small_one_tab()

def test_previwer_is_callable(selectable_simple_small1: Selectable):
    """
    Confirm sure that the preview callable can be called with
    a varianle number of selections, i.e *args but only of
    type Selectable.
    """

    s1 = selectable_simple_small1.excel_ref('C6:E7')
    s2 = selectable_simple_small1.excel_ref('A2:A10')
    s3 = selectable_simple_small1.excel_ref('G4:H4')
    s4 = selectable_simple_small1.excel_ref('G4:H4')
    s5 = selectable_simple_small1.excel_ref('G4:H4')

    preview(s1)
    preview(s1, s2, s3)
    preview(s1, s2, s3, s4, s5)

    with pytest.raises(AssertionError):
        preview(s1, s2, s3, True)

    with pytest.raises(AssertionError):
        preview([], s1)

    with pytest.raises(AssertionError):
        preview(s1, s2, None, s4, s5)
