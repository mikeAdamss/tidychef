# import pytest

# from pivoter.selection.base import Selectable
# from tests.fixtures.objects.selectables.selectable import (
#     single_table_input_A1,
#     single_excel_input_A1A2
# )

# def test_assert_one_with_single_cell(single_table_input_A1: Selectable):
#     """
#     Test assert one behaves correctly on a selection consisting
#     of one cell
#     """
#     single_table_input_A1.assert_one()


# def test_assert_one_without_single_cell(single_excel_input_A1A2: Selectable):
#     """
#     Test assert one behaves correctly on a selection not consisiting
#     of a single cell.
#     """

#     with pytest.raises(AssertionError):
#         single_excel_input_A1A2.assert_one()
