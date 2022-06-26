from typing import List

from datachef.models.source.cell import Cell


def cells_with_valid_values() -> List[Cell]:
    return [
        Cell(x=0, y=0, value="foo"),
        Cell(x=0, y=0, value="bar"),
        Cell(x=0, y=0, value="baz"),
        Cell(x=0, y=0, value="   stripme  "),
        Cell(x=0, y=0, value=""),
        Cell(x=0, y=0, value="    "),
        Cell(x=0, y=0, value=None),
    ]


def cells_with_invalid_values() -> List[Cell]:
    return [Cell(x=0, y=0, value=7.9), Cell(x=0, y=0, value=True)]
