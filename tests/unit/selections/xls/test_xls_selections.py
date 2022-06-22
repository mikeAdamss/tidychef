# import pytest

# from pivoter.models.source.cell import Cell
# from pivoter.selection.spreadsheet.xls import XlsInputSelectable
# from pivoter.exceptions import CellsDoNotExistError, LoneValueOnMultipleCellsError
# from tests.fixtures.objects.selectables.xls import XlsInputSelectable


# def test_lone_value_selector(single_excel_input_A1A3: XlsInputSelectable):
#     """
#     Test we can return the value for selections of exactly one cell
#     """
#     assert single_excel_input_A1A3.excel_ref("A1").lone_value() == "foo"


# def test_lone_value_on_multiple_values_errors(
#     single_excel_input_A1A3: XlsInputSelectable,
# ):
#     """
#     Test than calling Input.lone_value() on a filtered table containing
#     more than one value raises.
#     """

#     with pytest.raises(LoneValueOnMultipleCellsError):
#         single_excel_input_A1A3.lone_value()


# def test_excel_referece_out_of_bounds_error(
#     single_excel_input_A1A3: XlsInputSelectable,
# ):
#     """
#     Test that we cannot select using an excel reference for cells that
#     are not within the current selection
#     """

#     with pytest.raises(CellsDoNotExistError) as exc_info:
#         single_excel_input_A1A3.excel_ref("A1:D2")
