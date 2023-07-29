
import datetime
from typing import Any, Dict, List, Union

import xlrd

from tidychef.exceptions import UnknownExcelTimeError
from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.selectable import Selectable
from tidychef.selection.xls.xls import XlsSelectable

from ..excel_time import EXCEL_TIME_FORMATS, missing_time_format_message


def xls_time_formats():
    """
    Wrapped for test purposes
    """
    return EXCEL_TIME_FORMATS

def strip_non_time_formatting(pattern: str) -> str:
    """
    Do what we can to remove the random excel formatting information
    that'll interfere with discovering the time formatting.
    """

    # We'll do it with a split as the nonsence comes
    # after time
    for remove in ["@", ";"]:
        pattern = pattern.split(remove)[0]
    return pattern


def sheets_from_workbook(source: Any, selectable: Selectable, workbook: xlrd.book, custom_time_formats: Dict[str, str], **kwargs) -> Union[XlsSelectable, List[XlsSelectable]]:
    assert isinstance(workbook, xlrd.Book)

    tidychef_selectables = []
    worksheet_names = workbook.sheet_names()

    for worksheet_name in worksheet_names:
        worksheet = workbook.sheet_by_name(worksheet_name, **kwargs)

        table = Table()
        num_rows = worksheet.nrows

        for y in range(0, num_rows):
            for x, cell in enumerate(worksheet.row(y)):

                if cell.ctype == 3: # Date Cell
                    xf = workbook.xf_list[cell.xf_index]
                    xls_time_format = strip_non_time_formatting(workbook.format_map[xf.format_key].format_str)
                    strformat_pattern = xls_time_formats().get(xls_time_format, None)
                    if strformat_pattern is None:

                        strformat_pattern = custom_time_formats.get(xls_time_format, None)

                        if strformat_pattern is None:
                            raise UnknownExcelTimeError(missing_time_format_message(xls_time_format))
                    
                    cell_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(cell.value, xlrd.book.Book.datemode))
                    cell_value = cell_as_datetime.strftime(strformat_pattern)
                else:
                    cell_value = str(cell.value)
                table.add_cell(
                    Cell(x=x, y=y, value=cell_value if cell_value else "")
                )

        tidychef_selectables.append(
            selectable(table, source=source, name=worksheet_name)
        )
    return tidychef_selectables

