import copy
import pytest
from dataclasses import dataclass
from typing import List

from pivoter.cardinal.directions import UP, DOWN, LEFT, RIGHT, BaseDirection
from pivoter.models.source.cell import BaseCell, Cell
from pivoter.selection.base import Selectable
from pivotertesthelpers import single_table_test_input

def single_input_A1F5() -> Selectable:
    """
    A single table input, in excel terms A1:F5
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


def test_shift_left_and_right():
    """
    Test we can shift in the LEFT and RIGHT cardinal direction.
    """

    @dataclass
    class Case:
        desc: str
        direction: BaseDirection
        expected: List[BaseCell]
        length: int

    for case in [
        Case("Right one bare", RIGHT, [BaseCell(x=3, y=0)], 5),
        Case("Right one", RIGHT(1), [BaseCell(x=3, y=0)], 5),
        Case("Right two", RIGHT(2), [BaseCell(x=4, y=0)], 5)
    ]:
    
        data = single_input_A1F5()
        data.cells = data.datamethods._cells_on_x_index(data.cells, 2) # C1:C5

        data.shift(case.direction)

        for cell_to_find in case.expected:
            assert any([x.matches_xy(cell_to_find) for x in data.cells]), (
                f'Unable to find cell {cell_to_find} in {data.cells}, '
                f' with case "{case.desc}" and direction {case.direction}'
            )
        assert len(data.cells) == case.length
