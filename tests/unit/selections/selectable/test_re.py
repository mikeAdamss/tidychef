from dataclasses import dataclass
from typing import Optional

import pytest

from datachef import datafuncs as dfc
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_re_patterns(selectable_simple1: Selectable):
    """
    Test a selection of regular expressions with the re method
    """

    @dataclass
    class Case:
        with_ref: str  # Excel ref of our starting selection
        pattern: str  # Regular expression to apply to it
        expected_len: int  # Number of cells we expect to have after matching
        expected_ref: Optional[
            str
        ] = None  # Expected excel reference defning the cells after
        # matching. Optional so we can test selections
        # that have gaps or are not quadrilateral.

    # Please note: the cells in our fixture have the excel reference for
    # a value. So the cell value of cell position F5 is "F5".
    # it's these values that the re's are matching on.
    for case in [
        Case("F5:H15", "^[F-G].*$", 22, "F5:G15"),
        Case("F5:H15", "^(F|H).*$", 22),
    ]:

        # import re
        # raise Exception(re.match('^[F-G].*$', 'F5'))

        s = selectable_simple1.excel_ref(case.with_ref).re(case.pattern)
        assert len(s.cells) == case.expected_len

        # We either get the excel range we're expecting or we should
        # fail to assert its a quadrilateral selection
        if case.expected_ref:
            assert dfc.basecells_to_excel_ref(s.cells) == case.expected_ref
        else:
            with pytest.raises(AssertionError):
                dfc.assert_quadrilaterals(s.cells)
