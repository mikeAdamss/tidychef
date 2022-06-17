import pytest

from pivoter.constants import RIGHT, UP, DOWN, LEFT
from pivoter.models.source.cell import Cell
from pivoter.selection.base import Selectable
from ...helpers import single_table_test_input


@pytest.fixture
def single_input_A1F5() -> Selectable:
    """
    A single table input, one column of three cells for
    (in excel terms) A1:F5
    """
    return single_table_test_input(
        [
            Cell(x=0, y=0, value="of A1"),
            Cell(x=0, y=1, value="of A2"),
            Cell(x=0, y=2, value="of A3"),
            Cell(x=0, y=3, value="of A4"),
            Cell(x=0, y=4, value="of A5"),

            Cell(x=1, y=0, value="of B1"),
            Cell(x=1, y=1, value="of B2"),
            Cell(x=1, y=2, value="of B3"),
            Cell(x=1, y=3, value="of B4"),
            Cell(x=1, y=4, value="of B5"),

            Cell(x=2, y=0, value="of C1"),
            Cell(x=2, y=1, value="of C2"),
            Cell(x=2, y=2, value="of C3"),
            Cell(x=2, y=3, value="of C4"),
            Cell(x=2, y=4, value="of C5"),

            Cell(x=3, y=0, value="of D1"),
            Cell(x=3, y=1, value="of D2"),
            Cell(x=3, y=2, value="of D3"),
            Cell(x=3, y=3, value="of D4"),
            Cell(x=3, y=4, value="of D5"),

            Cell(x=4, y=0, value="of E1"),
            Cell(x=4, y=1, value="of E2"),
            Cell(x=4, y=2, value="of E3"),
            Cell(x=4, y=3, value="of E4"),
            Cell(x=4, y=4, value="of E5"),

            Cell(x=5, y=0, value="of F1"),
            Cell(x=5, y=1, value="of F2"),
            Cell(x=5, y=2, value="of F3"),
            Cell(x=5, y=3, value="of F4"),
            Cell(x=5, y=4, value="of F5"),
        ],
        "single fixture table A1:F5",
    )


def test_expand_1(single_input_A1F5: Selectable):
    
    single_input_A1F5.expand(RIGHT)