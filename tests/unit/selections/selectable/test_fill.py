# from dataclasses import dataclass
# from os import linesep
# from typing import List, Optional

# from pivoter.cardinal.directions import RIGHT, UP, DOWN, LEFT
# from pivoter.models.source.cell import BaseCell
# from pivoter.selection.base import Selectable
# from pivoter.selection import datafuncs as dfc
# from tests.fixtures.objects.selectables.selectable import single_input_A1F5


# def test_fill():
#     """
#     Test multiple variations of the fill command.
#     """

#     @dataclass
#     class Case:
#         """
#         Test Inputs for an extrusion (fill/expand) test.
#         """

#         name: str
#         starting_at: List[BaseCell]
#         direction: int
#         expected_count: int
#         data: Optional[Selectable] = None


#     for case in [
#         Case(
#             "F5, UP", [BaseCell(x=5, y=4)], UP, 4, single_input_A1F5()
#         ),
#         Case(
#             "C4, UP", [BaseCell(x=2, y=3)], UP, 3, single_input_A1F5()
#         ),
#         Case(
#             "A3, UP", [BaseCell(x=0, y=2)], UP, 2, single_input_A1F5()
#         ),
#         Case(
#             "A3 + F2, UP",
#             [BaseCell(x=0, y=2), BaseCell(x=5, y=1)],
#             UP,
#             3,
#             single_input_A1F5(),
#         ),
#         Case(
#             "A1, DOWN", [BaseCell(x=0, y=0)], DOWN, 4, single_input_A1F5()
#         ),
#         Case(
#             "C4, DOWN", [BaseCell(x=2, y=3)], DOWN, 1, single_input_A1F5()
#         ),
#         Case(
#             "A3, DOWN", [BaseCell(x=0, y=2)], DOWN, 2, single_input_A1F5()
#         ),
#         Case(
#             "A3 + F2, DOWN",
#             [BaseCell(x=0, y=2), BaseCell(x=5, y=1)],
#             DOWN,
#             5,
#             single_input_A1F5(),
#         ),
#         Case(
#             "B2, RIGHT", [BaseCell(x=1, y=1)], LEFT, 1, single_input_A1F5()
#         ),
#         Case(
#             "B4 + F5, LEFT",
#             [BaseCell(x=1, y=3), BaseCell(x=5, y=4)],
#             LEFT,
#             6,
#             single_input_A1F5(),
#         ),
#         Case(
#             "B2 + C3, LEFT",
#             [BaseCell(x=1, y=1), BaseCell(x=2, y=2)],
#             LEFT,
#             3,
#             single_input_A1F5(),
#         ),
#         Case(
#             "B2 + C3, RIGHT",
#             [BaseCell(x=1, y=1), BaseCell(x=2, y=2)],
#             RIGHT,
#             7,
#             single_input_A1F5(),
#         ),
#     ]:

#         case.data.cells = dfc.exactly_matched_xy_cells(
#             case.data.cells, case.starting_at
#         )

#         case.data.fill(case.direction)

#         assert len(case.data.cells) == case.expected_count, (
#             f"For {case.name} expected {case.expected_count} cells, got {len(case.data.cells)}: {linesep}"
#             f"{case.data.selected_table.filtered._as_xy_str()}"
#         )
