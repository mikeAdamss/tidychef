import pytest

from pivoter.models.source.cell import Cell
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from .helpers import single_table_test_input


@pytest.fixture
def single_excel_input_A1A3() -> XlsInputSelectable:
    """
    A single table input, one column of three cells for
    (in excel terms) A1:A3
    """
    return single_table_test_input(
        [
            Cell(x=0, y=0, value="foo"),
            Cell(x=0, y=1, value="bar"),
            Cell(x=0, y=2, value="baz"),
        ],
        "single fixture table 1",
        input_type=XlsInputSelectable,
    )
