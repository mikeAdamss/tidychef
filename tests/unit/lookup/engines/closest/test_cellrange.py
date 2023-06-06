from dataclasses import dataclass

from datachef.cardinal.directions import up, down, left, right
from datachef.lookup.engines.closest import CellRange
from datachef.models.source.cell import Cell
from tests.unit.helpers import qcel


def test_cell_range_contains_horizontally():
    """
    Test that the contains method returns as expected
    for a given horizontal range of cells.
    """

    # A random cell
    # Has no relevance here, just to satisfy constructor.
    unused_cell = Cell(x=0, y=0, value="_")

    # A range on the horizontal/x axis
    # denotes a range spanning columns F-J in excel terms
    cell_range = CellRange(
        low=5,  # F in excel terms
        high=10,  # K in excel terms
        cell=unused_cell,
        direction=right,
    )

    @dataclass
    class Case:
        excel_ref: str
        should_be_found: bool

    # Lookups that should be found
    for case in [
        Case(excel_ref="B1", should_be_found=False),
        Case(excel_ref="E1", should_be_found=False),
        Case(excel_ref="F1", should_be_found=True),
        Case(excel_ref="I1", should_be_found=True),
        Case(excel_ref="K1", should_be_found=True),
        Case(excel_ref="L1", should_be_found=False),
        Case(excel_ref="ZB1", should_be_found=False),
    ]:
        query_cell = qcel(case.excel_ref)
        assert case.should_be_found is cell_range.contains(
            query_cell
        ), f"""
                Cell '{query_cell}' from excel_ref '{case.excel_ref}'
                
                Should be '{case.should_be_found}' for .contains() in horizontal range
                of low '{cell_range.low}', high '{cell_range.high}' but is '{not case.should_be_found}'.
            """


def test_cell_range_contains_vertically():
    """
    Test that the contains method returns as expected
    for a given vertical range of cells.
    """

    # A random cell
    # Has no relevance here, just to satisfy constructor.
    unused_cell = Cell(x=0, y=0, value="_")

    # A range on the vertical/y axis
    # denotes a range spanning rows 5-10 in excel terms
    cell_range = CellRange(low=4, high=9, cell=unused_cell, direction=up)

    @dataclass
    class Case:
        excel_ref: str
        should_be_found: bool

    # Lookups that should be found
    for case in [
        Case(excel_ref="B1", should_be_found=False),
        Case(excel_ref="E3", should_be_found=False),
        Case(excel_ref="F4", should_be_found=False),
        Case(excel_ref="A5", should_be_found=True),
        Case(excel_ref="J10", should_be_found=True),
        Case(excel_ref="K11", should_be_found=False),
        Case(excel_ref="Z198928", should_be_found=False),
    ]:
        query_cell = qcel(case.excel_ref)
        assert case.should_be_found is cell_range.contains(
            query_cell
        ), f"""
                Cell '{query_cell}' from excel_ref '{case.excel_ref}'
                
                Should be '{case.should_be_found}' for .contains() in vertical range
                of low '{cell_range.low}', high '{cell_range.high}' but is '{not case.should_be_found}'.
            """


def test_cell_range_spans_higher_range_than_vertically():
    """
    Test the CellRange.spans_higher_range_than() method can correctly
    identify when it spans a higher range than a given cell
    on the vertical axis.
    """

    # A random cell
    # Has no relevance here, just to satisfy constructor.
    unused_cell = Cell(x=0, y=0, value="_")

    # A range on the vertical/y axis
    # denotes a range spanning rows 5-10 in excel terms
    cell_range = CellRange(low=4, high=9, cell=unused_cell, direction=up)

    @dataclass
    class Case:
        excel_ref: str
        is_lower_than_range: bool

    for case in [
        Case(excel_ref="A1", is_lower_than_range=True),
        Case(excel_ref="A3", is_lower_than_range=True),
        Case(excel_ref="A4", is_lower_than_range=True),
        Case(excel_ref="A5", is_lower_than_range=False),
        Case(excel_ref="A2001", is_lower_than_range=False),
    ]:
        query_cell = qcel(case.excel_ref)
        assert (
            cell_range.spans_higher_range_than(query_cell) is case.is_lower_than_range
        ), f"""
            Cell '{query_cell}' from excel reference {case.excel_ref}
            Direction is {cell_range.direction.name}, so {query_cell.y} is the relevant attribute.

            Returning as:
            cell_range.spans_higher_range_than(cell) == {not case.is_lower_than_range}

            For range:
            low: {cell_range.low}
            high: {cell_range.high}

            Expecting: {case.is_lower_than_range}.

            Note: Uses standard python slicing conventions, example:
            - 0 would be INSIDE a range of 0-9
            - 9 would be OUTSIDE a range of 0-9
            """


def test_cell_range_spans_lower_range_than_vertically():
    """
    Test the CellRange.spans_higher_range_than() method can correctly
    identify when it spans a higher range than a given cell
    on the vertical axis.
    """

    # A random cell
    # Has no relevance here, just to satisfy constructor.
    unused_cell = Cell(x=0, y=0, value="_")

    # A range on the vertical/y axis
    # denotes a range spanning rows 5-10 in excel terms
    cell_range = CellRange(low=4, high=9, cell=unused_cell, direction=down)

    @dataclass
    class Case:
        excel_ref: str
        is_higher_than_range: bool

    for case in [
        Case(excel_ref="A1", is_higher_than_range=False),
        Case(excel_ref="A9", is_higher_than_range=False),
        Case(excel_ref="A10", is_higher_than_range=False),
        Case(excel_ref="A11", is_higher_than_range=True),
    ]:
        query_cell = qcel(case.excel_ref)
        assert (
            cell_range.spans_lower_range_than(query_cell) is case.is_higher_than_range
        ), f"""
            Cell '{query_cell}' from excel reference {case.excel_ref}
            Direction is {cell_range.direction.name}, so {query_cell.y} is the relevant attribute.

            Returning as:
            cell_range.spans_higher_range_than(cell) == {not case.is_higher_than_range}

            For range:
            low: {cell_range.low}
            high: {cell_range.high}

            Expecting: {case.is_higher_than_range}.

            Note: Uses standard python slicing conventions, example:
            - 0 would be INSIDE a range of 0-9
            - 9 would be OUTSIDE a range of 0-9
            """


def test_cell_range_spans_lower_range_than_horizontally():
    """
    Test the CellRange.spans_lower_range_than() method can correctly
    identify when it spans a lower range than a given cell
    on the horizontal axis.
    """

    # A random cell
    # Has no relevance here, just to satisfy constructor.
    unused_cell = Cell(x=0, y=0, value="_")

    # A range on the vertical/y axis
    # denotes a range spanning rows 5-10 in excel terms
    cell_range = CellRange(
        low=5, high=10, cell=unused_cell, direction=right  # F  # K
    )

    @dataclass
    class Case:
        excel_ref: str
        is_higher_than_range: bool

    for case in [
        Case(excel_ref="A1", is_higher_than_range=False),
        Case(excel_ref="F3", is_higher_than_range=False),
        Case(excel_ref="J4", is_higher_than_range=False),
        Case(excel_ref="K5", is_higher_than_range=False),
        Case(excel_ref="L5", is_higher_than_range=True)
    ]:
        query_cell = qcel(case.excel_ref)
        assert (
            cell_range.spans_lower_range_than(query_cell) is case.is_higher_than_range
        ), f"""
            Cell '{query_cell}' from excel reference {case.excel_ref}
            Direction is {cell_range.direction.name}, so {query_cell.y} is the relevant attribute.

            Returning as:
            cell_range.spans_higher_range_than(cell) == {not case.is_higher_than_range}

            For range:
            low: {cell_range.low}
            high: {cell_range.high}

            Expecting: {case.is_higher_than_range}.

            Note: Uses standard python slicing conventions, example:
            - E would be OUTSIDE a range of F-K
            - F would be INSIDE a range of F-K
            - J would be INSIDE a range of F-K
            - K would be OUTSIDE a range of F-K
            """


def test_cell_range_spans_higher_range_than_horizontally():
    """
    Test the CellRange.spans_higher_range_than() method can correctly
    identify when it spans a higher range than a given cell
    on the vertical axis.
    """

    # A random cell
    # Has no relevance here, just to satisfy constructor.
    unused_cell = Cell(x=0, y=0, value="_")

    # A range on the vertical/y axis
    # denotes a range spanning rows 5-10 in excel terms
    cell_range = CellRange(
        low=5, high=10, cell=unused_cell, direction=left  # F  # K
    )

    @dataclass
    class Case:
        excel_ref: str
        is_lower_than_range: bool

    for case in [
        Case(excel_ref="A1", is_lower_than_range=True),
        Case(excel_ref="E3", is_lower_than_range=True),
        Case(excel_ref="F4", is_lower_than_range=False),
        Case(excel_ref="K5", is_lower_than_range=False),
    ]:
        query_cell = qcel(case.excel_ref)
        assert (
            cell_range.spans_higher_range_than(query_cell) is case.is_lower_than_range
        ), f"""
            Cell '{query_cell}' from excel reference {case.excel_ref}
            Direction is {cell_range.direction.name}, so {query_cell.y} is the relevant attribute.

            Returning as:
            cell_range.spans_higher_range_than(cell) == {not case.is_lower_than_range}

            For range:
            low: {cell_range.low}
            high: {cell_range.high}

            Expecting: {case.is_lower_than_range}.

            Note: Uses standard python slicing conventions, example:
            - E would be OUTSIDE a range of F-K
            - F would be INSIDE a range of F-K
            - J would be INSIDE a range of F-K
            - K would be OUTSIDE a range of F-K
            """
