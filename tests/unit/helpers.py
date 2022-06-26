from typing import List

from pivoter.models.source.cell import BaseCell
from pivoter.selection import datafuncs as dfc


def qcel(excel_ref) -> BaseCell:
    """
    "QueryCell" - test helper to create a single BaseCell object from
    an appropriate excel reference.
    """
    assert ":" not in excel_ref
    cell: BaseCell = dfc.single_excel_ref_to_basecell(excel_ref)
    return cell


def qcels(excel_ref) -> List[BaseCell]:
    """
    "QueryCells" - test helper to create a list of 2 or more BaseCell objects from
    an appropriate excel reference.
    """
    assert ":" in excel_ref
    cells: List[BaseCell] = dfc.multi_excel_ref_to_basecells(excel_ref)
    return cells
