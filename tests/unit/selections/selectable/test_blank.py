# import pytest

# from pivoter.models.source.cell import Cell
# from pivoter.selection.base import Selectable
# from tests.fixtures.objects.selectables.selectable import single_input_mixed_blank_and_not

# def test_all_blanks_from_table(single_input_mixed_blank_and_not: Selectable):
#     """
#     Test that default blank behaviour filters to all expected cells.
#     """
#     single_input_mixed_blank_and_not.is_blank()
#     assert len(single_input_mixed_blank_and_not.cells) == 4


# def test_all_blanks_from_table_not_disregarding_whitespace(
#     single_input_mixed_blank_and_not: Selectable,
# ):
#     """
#     Test that default blank behaviour filters to all expected cells.
#     """
#     single_input_mixed_blank_and_not.is_blank(disregard_whitespace=False)
#     assert len(single_input_mixed_blank_and_not.cells) == 2


# def test_all_non_blanks_from_table(single_input_mixed_blank_and_not: Selectable):
#     """
#     Test that default non blank behaviour filters to all expected cells.
#     """
#     single_input_mixed_blank_and_not.is_not_blank()
#     assert len(single_input_mixed_blank_and_not.cells) == 3
