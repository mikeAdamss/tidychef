import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef import against
from tidychef.exceptions import CellValidationError
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_selection_validation(selectable_simple1: Selectable):
    """
    Test that the validate() correctly raises the expected
    exception.
    """

    with pytest.raises(CellValidationError):
        selectable_simple1.excel_ref("B1").validate(against.regex("A1val"))

    with pytest.raises(CellValidationError):
        selectable_simple1.excel_ref("B1").validate(
            against.regex("A1val"), raise_first_error=True
        )

    selectable_simple1.excel_ref("B1").validate(against.regex("B1val"))
