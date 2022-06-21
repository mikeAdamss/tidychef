from os import linesep

from pivoter.cardinal.directions import RIGHT, UP, DOWN, LEFT
from pivoter.models.source.cell import Cell, BaseCell
from pivoter.selection.base import Selectable
from pivoter.selection import datafuncs as dfc
from pivotertesthelpers import single_table_test_input, InputsToTestExtrusion


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


def test_fill():
    """
    Test multiple variations of the fill command.
    """

    for case in [
        InputsToTestExtrusion(
            "F5, UP", [BaseCell(x=5, y=4)], UP, 4, single_input_A1F5()
        ),
        InputsToTestExtrusion(
            "C4, UP", [BaseCell(x=2, y=3)], UP, 3, single_input_A1F5()
        ),
        InputsToTestExtrusion(
            "A3, UP", [BaseCell(x=0, y=2)], UP, 2, single_input_A1F5()
        ),
        InputsToTestExtrusion(
            "A3 + F2, UP",
            [BaseCell(x=0, y=2), BaseCell(x=5, y=1)],
            UP,
            3,
            single_input_A1F5(),
        ),
        InputsToTestExtrusion(
            "A1, DOWN", [BaseCell(x=0, y=0)], DOWN, 4, single_input_A1F5()
        ),
        InputsToTestExtrusion(
            "C4, DOWN", [BaseCell(x=2, y=3)], DOWN, 1, single_input_A1F5()
        ),
        InputsToTestExtrusion(
            "A3, DOWN", [BaseCell(x=0, y=2)], DOWN, 2, single_input_A1F5()
        ),
        InputsToTestExtrusion(
            "A3 + F2, DOWN",
            [BaseCell(x=0, y=2), BaseCell(x=5, y=1)],
            DOWN,
            5,
            single_input_A1F5(),
        ),
        InputsToTestExtrusion(
            "B2, RIGHT", [BaseCell(x=1, y=1)], LEFT, 1, single_input_A1F5()
        ),
        InputsToTestExtrusion(
            "B4 + F5, LEFT",
            [BaseCell(x=1, y=3), BaseCell(x=5, y=4)],
            LEFT,
            6,
            single_input_A1F5(),
        ),
        InputsToTestExtrusion(
            "B2 + C3, LEFT",
            [BaseCell(x=1, y=1), BaseCell(x=2, y=2)],
            LEFT,
            3,
            single_input_A1F5(),
        ),
        InputsToTestExtrusion(
            "B2 + C3, RIGHT",
            [BaseCell(x=1, y=1), BaseCell(x=2, y=2)],
            RIGHT,
            7,
            single_input_A1F5(),
        ),
    ]:

        case.data.cells = dfc.exactly_matched_xy_cells(
            case.data.cells, case.starting_at
        )

        case.data.fill(case.direction)

        assert len(case.data.cells) == case.expected_count, (
            f"For {case.name} expected {case.expected_count} cells, got {len(case.data.cells)}: {linesep}"
            f"{case.data.selected_table.filtered._as_xy_str()}"
        )
