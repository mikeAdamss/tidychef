from typing import List

from pivoter.models.source.cell import BaseCell
from pivoter.utils import cellutils


def qcel(excel_ref) -> BaseCell:
    """
    "QueryCell" - test helper to create a single BaseCell object from
    an appropriate excel reference.
    """
    assert ":" not in excel_ref
    cells: List[BaseCell] = cellutils.excel_ref_as_wanted_basecells(excel_ref)
    assert len(cells) == 1
    return cells[0]


def qcels(excel_ref) -> List[BaseCell]:
    """
    "QueryCells" - test helper to create a list of 2 or more BaseCell objects from
    an appropriate excel reference.
    """
    assert ":" in excel_ref
    cells: List[BaseCell] = cellutils.excel_ref_as_wanted_basecells(excel_ref)
    return cells
