from pathlib import Path
from typing import List

from tests.fixtures import path_to_fixture  
from tidychef import acquire
from tidychef.models.source.cellformat import CellFormatting
from tidychef.selection.xlsx.xlsx import XlsxSelectable


def test_acquire_local_xlsx():
    """
    Test that the acquire function works with a local xls
    """

    xlsx_path = path_to_fixture("xlsx", "ons-oic.xlsx")
    assert isinstance(acquire.xlsx.local(xlsx_path)[0], XlsxSelectable)

    xlsx_path_as_str = xlsx_path.resolve()
    assert isinstance(acquire.xlsx.local(xlsx_path_as_str)[0], XlsxSelectable)


def test_read_local_xlsx_from_path():
    """
    Test local file loader for xls from path
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[3]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 4455


def test_read_local_xlsx_from_str():
    """
    Test local file loader for csv from str
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(str(xlsx_path.absolute()))
    sheet = sheets[3]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 4455


def test_unknown_xlsx_local_time_format_can_be_specified(mocker):
    """
    Test that were we don't have knowledge of an xlsx time
    format string the user can explicitly pass in a
    formatting string.
    """

    mocker.patch("tidychef.acquire.xlsx.shared.xlsx_time_formats", return_value={})

    xlsx_path: Path = path_to_fixture("xlsx", "dates-times.xlsx")
    sheet: XlsxSelectable = acquire.xlsx.local(
        xlsx_path,
        tables="Sheet1",
        custom_time_formats={"d/m/yyyy": "%d/%m/%y"},
    )

    assert [x.value for x in sheet.pcells] == [
        "dates",
        "11/01/23",
        "11/01/23",
        "12/01/22",
        "10/10/00",
        "",
    ]


def test_xlsx_cells_have_complete_formatting_information():
    """
    Test that all cells in XLSX files have CellFormatting objects with all formatting properties.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    # Use Cover Sheet (index 0) which has known formatting
    sheet = sheets[0]
    
    # All cells should have complete formatting information
    for cell in sheet.cells:
        assert cell.cellformat is not None, f"Cell at ({cell.x}, {cell.y}) lacks formatting information"
        assert isinstance(cell.cellformat, CellFormatting), f"Cell at ({cell.x}, {cell.y}) has wrong formatting type"
        assert isinstance(cell.cellformat.bold, bool), f"Cell at ({cell.x}, {cell.y}) bold property is not boolean"
        assert isinstance(cell.cellformat.italic, bool), f"Cell at ({cell.x}, {cell.y}) italic property is not boolean"
        assert isinstance(cell.cellformat.underline, bool), f"Cell at ({cell.x}, {cell.y}) underline property is not boolean"
        assert isinstance(cell.cellformat.hyperlink, bool), f"Cell at ({cell.x}, {cell.y}) hyperlink property is not boolean"
        assert isinstance(cell.cellformat.indent_level, int), f"Cell at ({cell.x}, {cell.y}) indent_level property is not integer"
        assert cell.cellformat.indent_level >= 0, f"Cell at ({cell.x}, {cell.y}) indent_level should be non-negative"


def test_xlsx_bold_cell_detection():
    """
    Test that known bold cells are correctly detected as bold.
    Cell A1 (x=0, y=0) in Cover Sheet should be bold.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Find cell A1 (x=0, y=0) which should be bold
    a1_cell = None
    for cell in sheet.cells:
        if cell.x == 0 and cell.y == 0:
            a1_cell = cell
            break
    
    assert a1_cell is not None, "Could not find cell A1"
    assert "Output in the construction industry" in a1_cell.value, f"Expected title content, got '{a1_cell.value}'"
    assert a1_cell.cellformat is not None, "Cell A1 lacks formatting information"
    assert a1_cell.cellformat.bold is True, "Cell A1 should be bold but is detected as not bold"


def test_xlsx_italic_cell_detection():
    """
    Test that italic cells are correctly detected.
    Cell B8 (x=1, y=7) in Cover Sheet should be italic.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Find cell B8 (x=1, y=7) which should be italic
    b8_cell = None
    for cell in sheet.cells:
        if cell.x == 1 and cell.y == 7:
            b8_cell = cell
            break
    
    assert b8_cell is not None, "Could not find cell B8"
    assert b8_cell.cellformat is not None, "Cell B8 lacks formatting information"
    assert b8_cell.cellformat.italic is True, "Cell B8 should be italic"
    assert b8_cell.cellformat.is_italic() is True, "Cell B8 is_italic() should return True"


def test_xlsx_underline_cell_detection():
    """
    Test that underlined cells are correctly detected.
    Cell A12 (x=0, y=11) in Cover Sheet should be underlined.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Find cell A12 (x=0, y=11) which should be underlined
    a12_cell = None
    for cell in sheet.cells:
        if cell.x == 0 and cell.y == 11:
            a12_cell = cell
            break
    
    assert a12_cell is not None, "Could not find cell A12"
    assert a12_cell.cellformat is not None, "Cell A12 lacks formatting information"
    assert a12_cell.cellformat.underline is True, "Cell A12 should be underlined"
    assert a12_cell.cellformat.is_underline() is True, "Cell A12 is_underline() should return True"


def test_xlsx_hyperlink_cell_detection():
    """
    Test that hyperlink cells are correctly detected.
    Cell B11 (x=1, y=10) in Cover Sheet should be a hyperlink.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Find cell B11 (x=1, y=10) which should be a hyperlink
    b11_cell = None
    for cell in sheet.cells:
        if cell.x == 1 and cell.y == 10:
            b11_cell = cell
            break
    
    assert b11_cell is not None, "Could not find cell B11"
    assert b11_cell.cellformat is not None, "Cell B11 lacks formatting information"
    assert b11_cell.cellformat.hyperlink is True, "Cell B11 should be hyperlink"
    assert b11_cell.cellformat.is_hyperlink() is True, "Cell B11 is_hyperlink() should return True"


def test_xlsx_non_formatted_cell_detection():
    """
    Test that non-formatted cells are correctly detected.
    Most cells should not have specific formatting.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Find a cell that should not have special formatting (e.g., A3)
    a3_cell = None
    for cell in sheet.cells:
        if cell.x == 0 and cell.y == 2:
            a3_cell = cell
            break
    
    assert a3_cell is not None, "Could not find cell A3"
    assert a3_cell.cellformat is not None, "Cell A3 lacks formatting information"
    # These should be False for a normal cell
    assert a3_cell.cellformat.bold is False, "Cell A3 should not be bold"
    assert a3_cell.cellformat.italic is False, "Cell A3 should not be italic"
    assert a3_cell.cellformat.hyperlink is False, "Cell A3 should not be hyperlink"


def test_xlsx_indented_cell_detection():
    """
    Test that indented cells are correctly detected.
    Cell A2 (x=0, y=1) in Cover Sheet should be indented with level 1.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Find cell A2 (x=0, y=1) which should be indented
    a2_cell = None
    for cell in sheet.cells:
        if cell.x == 0 and cell.y == 1:
            a2_cell = cell
            break
    
    assert a2_cell is not None, "Could not find cell A2"
    assert a2_cell.cellformat is not None, "Cell A2 lacks formatting information"
    assert a2_cell.cellformat.indent_level == 1, "Cell A2 should have indent level 1"
    assert a2_cell.cellformat.is_indented() is True, "Cell A2 is_indented() should return True"
    assert a2_cell.cellformat.get_indent_level() == 1, "Cell A2 get_indent_level() should return 1"


def test_xlsx_formatting_methods():
    """
    Test that formatting methods work correctly on cells with known formatting status.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Find the bold cell A1 and non-bold cell A3
    a1_cell = None
    a3_cell = None
    for cell in sheet.cells:
        if cell.x == 0 and cell.y == 0:  # A1
            a1_cell = cell
        elif cell.x == 0 and cell.y == 2:  # A3
            a3_cell = cell
    
    assert a1_cell is not None, "Could not find cell A1"
    assert a3_cell is not None, "Could not find cell A3"
    
    # Test is_bold() method
    assert a1_cell.cellformat.is_bold() is True, "Cell A1 is_bold() should return True"
    assert a3_cell.cellformat.is_bold() is False, "Cell A3 is_bold() should return False"


def test_xlsx_formatting_selection_methods():
    """
    Test that all the formatting selection methods work correctly.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Test bold selection methods
    bold_cells = sheet.is_bold()
    not_bold_cells = sheet.is_not_bold()
    assert len(bold_cells.cells) == 1, "Should find exactly 1 bold cell (A1)"
    assert len(not_bold_cells.cells) > 0, "Should find some non-bold cells"
    assert len(bold_cells.cells) + len(not_bold_cells.cells) == len(sheet.cells), "Bold + not bold should equal total"
    
    # Test italic selection methods
    italic_cells = sheet.is_italic()
    not_italic_cells = sheet.is_not_italic()
    assert len(italic_cells.cells) == 1, "Should find exactly 1 italic cell (B8)"
    assert len(not_italic_cells.cells) > 0, "Should find some non-italic cells"
    assert len(italic_cells.cells) + len(not_italic_cells.cells) == len(sheet.cells), "Italic + not italic should equal total"
    
    # Test underline selection methods
    underline_cells = sheet.is_underline()
    not_underline_cells = sheet.is_not_underline()
    assert len(underline_cells.cells) == 2, "Should find exactly 2 underlined cells (A12, B11)"
    assert len(not_underline_cells.cells) > 0, "Should find some non-underlined cells"
    assert len(underline_cells.cells) + len(not_underline_cells.cells) == len(sheet.cells), "Underline + not underline should equal total"
    
    # Test hyperlink selection methods
    hyperlink_cells = sheet.is_hyperlink()
    not_hyperlink_cells = sheet.is_not_hyperlink()
    assert len(hyperlink_cells.cells) == 1, "Should find exactly 1 hyperlink cell (B11)"
    assert len(not_hyperlink_cells.cells) > 0, "Should find some non-hyperlink cells"
    assert len(hyperlink_cells.cells) + len(not_hyperlink_cells.cells) == len(sheet.cells), "Hyperlink + not hyperlink should equal total"
    
    # Test indentation selection methods (A2 is indented with level 1)
    indented_cells = sheet.is_indented()
    not_indented_cells = sheet.is_not_indented()
    assert len(indented_cells.cells) == 1, "Should find exactly 1 indented cell (A2)"
    assert len(not_indented_cells.cells) > 0, "Should find some non-indented cells"
    assert len(indented_cells.cells) + len(not_indented_cells.cells) == len(sheet.cells), "Indented + not indented should equal total"
    
    # Verify A2 is the indented cell
    a2_found = False
    for cell in indented_cells.cells:
        if cell.x == 0 and cell.y == 1:  # A2
            a2_found = True
            break
    assert a2_found, "A2 should be found in indented cells selection"


def test_xlsx_formatting_preserves_existing_functionality():
    """
    Test that adding formatting doesn't break existing cell functionality.
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[0]  # Cover Sheet
    
    # Verify basic functionality still works
    assert len(sheet.cells) > 0, "Should have cells"
    assert sheet.cells == sheet.pcells, "Cells and pcells should still be equal"
    
    # Verify we can still access cell values and positions
    for cell in sheet.cells:
        assert hasattr(cell, 'x'), "Cell should have x coordinate"
        assert hasattr(cell, 'y'), "Cell should have y coordinate"
        assert hasattr(cell, 'value'), "Cell should have value"
        assert isinstance(cell.x, int), "Cell x should be integer"
        assert isinstance(cell.y, int), "Cell y should be integer"
        assert isinstance(cell.value, str), "Cell value should be string"
