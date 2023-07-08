import pytest

from datachef import against
from datachef.exceptions import CellValidationError
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_selection_validation(selectable_simple1: Selectable):
    """
    Test that the validate() correctly raises the expected
    exception.
    """

    with pytest.raises(CellValidationError):
        selectable_simple1.excel_ref("B1").validate(against.regex('A1val'))


