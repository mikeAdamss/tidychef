# from dataclasses import dataclass
# from typing import List

# from pivoter.utils import cellutils
# from pivoter.models.source.cell import BaseCell


# def test_excel_ref_to_x():
#     """
#     Given excel references, return an x co-ordinate
#     """

#     for excel_ref, expected_x in [
#         ["A", 0],
#         ["AA", 26],
#         ["AAA", 52],
#         ["AB", 27],
#         ["DFG", 58],
#     ]:
#         got: int = cellutils.letter_to_x(excel_ref)
#         assert expected_x == got, f"Expected {expected_x}, got {got}"


# def test_excel_row_to_y():
#     """
#     Test converting an excel row number into a y offset
#     """
#     assert cellutils.number_to_y(7) == 6


# def test_y_to_excel_row():
#     """
#     Test converting an excel row number into a y offset
#     """
#     assert cellutils.y_to_number(6) == 7


# def test_single_excel_ref():
#     """
#     Given a single cell excel reference, return the correct
#     BaseCell
#     """

#     for excel_ref, expected in [
#         ["A1", BaseCell(0, 0)],
#         ["C17", BaseCell(2, 16)],
#         ["DFG200", BaseCell(58, 199)],
#     ]:
#         assert cellutils.single_excel_ref_to_basecells(excel_ref) == expected


# def test_multiple_excel_ref():
#     """
#     Given a single cell excel reference, return a list of the correct BaseCell's.
#     """

#     expected: List
#     for excel_ref, expected in [["A1:A2", [BaseCell(0, 0), BaseCell(0, 1)]]]:
#         cells_from_excel_ref: List[BaseCell] = cellutils.multi_excel_ref_to_basecells(
#             excel_ref
#         )
#         msg = f"""
#             Expected cells:
#             {expected}

#             Got Cells
#             {cells_from_excel_ref}
#             """

#         for ec in expected:
#             assert ec in cells_from_excel_ref, msg
#         assert len(expected) == len(cells_from_excel_ref), msg


# def test_x_to_letters():
#     """
#     Given an x co-ordinate, covert that co-ordinate to the
#     excel letters represnting it as a column
#     """

#     @dataclass
#     class Case:
#         x: int
#         expected: str

#     for case in [Case(5, "F"), Case(26, "AA"), Case(25, "Z"), Case(51, "AZ")]:
#         assert (
#             cellutils.x_to_letters(case.x) == case.expected
#         ), f"Expected {case.expected} from x:{case.x}, but got {cellutils.x_to_letters(case.x)}"


# def test_excel_ref_to_basecells():
#     """
#     Confirm that excel references can correctly be converted to lists of BaseCells
#     """

#     @dataclass
#     class Case:
#         excel_ref: str
#         cells: List[BaseCell]

#     for case in [
#         Case("A1:B1", [BaseCell(x=0, y=0), BaseCell(x=1, y=0)]),
#         Case(
#             "A2:C3",
#             [
#                 BaseCell(x=0, y=1),
#                 BaseCell(x=0, y=2),
#                 BaseCell(x=1, y=1),
#                 BaseCell(x=1, y=2),
#                 BaseCell(x=2, y=1),
#                 BaseCell(x=2, y=2),
#             ],
#         ),
#         Case("ZB1", [BaseCell(x=27, y=0)]),
#     ]:

#         cells: List[BaseCell] = cellutils.excel_ref_as_wanted_basecells(case.excel_ref)

#         assert len(cells) == len(case.cells), (
#             "Excel ref resulting in unexpected number of cell references. "
#             f"Got {len(cells)}, expecting {len()}"
#         )

#         for cell in cells:
#             assert (
#                 cell in case.cells
#             ), f"Cell {cell} missing from expected cells {case.cells}"

#         for cell in case.cells:
#             assert cell in cells, f"Cell {cell} missing from expected cells {cells}"
