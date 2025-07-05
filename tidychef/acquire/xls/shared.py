import datetime
import logging
import re
from typing import Any, Dict, List, Union

import xlrd

from tidychef.models.source.cell import Cell
from tidychef.models.source.table import Table
from tidychef.selection.selectable import Selectable
from tidychef.selection.xls.xls import XlsSelectable

from ..excel_time import EXCEL_TIME_FORMATS


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


def sheets_from_workbook(
    source: Any,
    selectable: Selectable,
    workbook: xlrd.book,
    custom_time_formats: Dict[str, str],
    tables_regex: str,
    **kwargs,
) -> Union[XlsSelectable, List[XlsSelectable]]:
    assert isinstance(workbook, xlrd.Book)

    tidychef_selectables = []
    worksheet_names = workbook.sheet_names()

    for worksheet_name in worksheet_names:
        time_format_warnings = {}

        if tables_regex is not None:
            if not re.match(tables_regex, worksheet_name):
                continue
        worksheet = workbook.sheet_by_name(worksheet_name, **kwargs)

        table = Table()
        num_rows = worksheet.nrows

        for y in range(0, num_rows):
            for x, cell in enumerate(worksheet.row(y)):

                if cell.ctype == 3:  # Date Cell
                    xf = workbook.xf_list[cell.xf_index]
                    xls_time_format = strip_non_time_formatting(
                        workbook.format_map[xf.format_key].format_str
                    )
                    strformat_pattern = xls_time_formats().get(xls_time_format, None)
                    if strformat_pattern is None:

                        strformat_pattern = custom_time_formats.get(
                            xls_time_format, None
                        )

                        if strformat_pattern is None:
                            xy = f"x:{x}, y:{y}"
                            if xls_time_format not in time_format_warnings:
                                time_format_warnings[xls_time_format] = []
                            time_format_warnings[xls_time_format].append(xy)
                            cell_value = cell.value
                        else:
                            cell_as_datetime = datetime.datetime(
                                *xlrd.xldate_as_tuple(
                                    cell.value, xlrd.book.Book.datemode
                                )
                            )
                            cell_value = cell_as_datetime.strftime(strformat_pattern)
                    else:
                        cell_as_datetime = datetime.datetime(
                            *xlrd.xldate_as_tuple(cell.value, xlrd.book.Book.datemode)
                        )
                        cell_value = cell_as_datetime.strftime(strformat_pattern)
                else:
                    cell_value = str(cell.value)
                table.add_cell(Cell(x=x, y=y, value=cell_value if cell_value else ""))

        for bad_fmt, examples in time_format_warnings.items():
            time_issue_cells = (
                ",".join(examples[:5]) if len(examples) > 5 else ",".join(examples)
            )
            logging.warning(
                f"""When processing table "{worksheet_name}" an unknown excel time format "{bad_fmt}" was encountered. Using raw cell value instead. 
For more details on handling excel time formatting see tidychef documentation. Cell(s) in question (max 5 shown): {time_issue_cells}"""
            )

        tidychef_selectables.append(
            selectable(table, source=source, name=worksheet_name)
        )

    return tidychef_selectables
