from pathlib import Path
from typing import List

import pytest
from pytest_mock import mocker

from tests.fixtures import path_to_fixture
from tidychef import acquire
from tidychef.models.source.cellformat import CellFormatting
from tidychef.selection.xls.xls import XlsSelectable


def test_acquire_local_xls():
    """
    Test that the acquire function works with a local xls
    """

    xls_path = path_to_fixture("xls", "sample.xls")
    assert isinstance(acquire.xls.local(xls_path)[0], XlsSelectable)

    xls_path_as_str = xls_path.resolve()
    assert isinstance(acquire.xls.local(xls_path_as_str)[0], XlsSelectable)


def test_read_local_xls_from_path():
    """
    Test local file loader for xls from path
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 51


def test_read_local_xls_from_str():
    """
    Test local file loader for csv from str
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(str(xls_path.absolute()))
    sheet = sheets[0]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 51


def test_shared_xls_local_time_formatting_works():
    """
    Test that the xls time_format keyword works as expected.
    """

    xls_path: Path = path_to_fixture("xls", "dates-times.xls")
    sheet: XlsSelectable = acquire.xls.local(xls_path, tables="Sheet1")
    assert [x.value for x in sheet.pcells] == [
        "dates",
        "11/01/23",
        "11/01/23",
        "12/01/22",
        "10/10/00",
    ]


def test_xls_cells_have_complete_formatting_information():
    """
    Test that all cells in XLS files have CellFormatting objects with all formatting properties.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
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


def test_xls_bold_cell_detection():
    """
    Test that known bold cells are correctly detected as bold.
    Cell C5 (x=2, y=4) in sample.xls should be bold.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C5 (x=2, y=4) which should be bold
    c5_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 4:
            c5_cell = cell
            break
    
    assert c5_cell is not None, "Could not find cell C5"
    assert c5_cell.value == "Online Instruction Page", f"Expected 'Online Instruction Page', got '{c5_cell.value}'"
    assert c5_cell.cellformat is not None, "Cell C5 lacks formatting information"
    assert c5_cell.cellformat.bold is True, "Cell C5 should be bold but is detected as not bold"


def test_xls_non_bold_cell_detection():
    """
    Test that known non-bold cells are correctly detected as not bold.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C6 (x=2, y=5) which should not be bold
    c6_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 5:
            c6_cell = cell
            break
    
    assert c6_cell is not None, "Could not find cell C6"
    assert c6_cell.value == "Sample Data for Excel", f"Expected 'Sample Data for Excel', got '{c6_cell.value}'"
    assert c6_cell.cellformat is not None, "Cell C6 lacks formatting information"
    assert c6_cell.cellformat.bold is False, "Cell C6 should not be bold but is detected as bold"


def test_xls_bold_formatting_is_bold_method():
    """
    Test that the is_bold() method works correctly on cells with known bold status.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find the bold cell C5
    c5_cell = None
    c6_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 4:  # C5
            c5_cell = cell
        elif cell.x == 2 and cell.y == 5:  # C6
            c6_cell = cell
    
    assert c5_cell is not None, "Could not find cell C5"
    assert c6_cell is not None, "Could not find cell C6"
    
    # Test is_bold() method
    assert c5_cell.cellformat.is_bold() is True, "Cell C5 is_bold() should return True"
    assert c6_cell.cellformat.is_bold() is False, "Cell C6 is_bold() should return False"


def test_xls_formatting_preserves_existing_functionality():
    """
    Test that adding bold formatting doesn't break existing cell functionality.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Verify basic functionality still works
    assert len(sheet.cells) == 51, "Cell count should remain unchanged"
    assert sheet.cells == sheet.pcells, "Cells and pcells should still be equal"
    
    # Verify we can still access cell values and positions
    for cell in sheet.cells:
        assert hasattr(cell, 'x'), "Cell should have x coordinate"
        assert hasattr(cell, 'y'), "Cell should have y coordinate"
        assert hasattr(cell, 'value'), "Cell should have value"
        assert isinstance(cell.x, int), "Cell x should be integer"
        assert isinstance(cell.y, int), "Cell y should be integer"
        assert isinstance(cell.value, str), "Cell value should be string"


def test_xls_italic_cell_detection():
    """
    Test that italic cells are correctly detected.
    Cell C16 (x=2, y=15) in sample.xls should be italic.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C16 (x=2, y=15) which should be italic
    c16_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 15:
            c16_cell = cell
            break
    
    assert c16_cell is not None, "Could not find cell C16"
    assert c16_cell.cellformat is not None, "Cell C16 lacks formatting information"
    assert c16_cell.cellformat.italic is True, "Cell C16 should be italic"
    assert c16_cell.cellformat.is_italic() is True, "Cell C16 is_italic() should return True"


def test_xls_underline_cell_detection():
    """
    Test that underlined cells are correctly detected.
    Cell C17 (x=2, y=16) in sample.xls should be underlined.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C17 (x=2, y=16) which should be underlined
    c17_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 16:
            c17_cell = cell
            break
    
    assert c17_cell is not None, "Could not find cell C17"
    assert c17_cell.cellformat is not None, "Cell C17 lacks formatting information"
    assert c17_cell.cellformat.underline is True, "Cell C17 should be underlined"
    assert c17_cell.cellformat.is_underline() is True, "Cell C17 is_underline() should return True"


def test_xls_hyperlink_cell_detection():
    """
    Test that hyperlink cells are correctly detected.
    Cells C6, C10, C11, C12 in sample.xls should be hyperlinks.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Test hyperlink cells
    hyperlink_positions = [(2, 5), (2, 9), (2, 10), (2, 11)]  # C6, C10, C11, C12
    hyperlink_refs = ["C6", "C10", "C11", "C12"]
    
    for (x, y), ref in zip(hyperlink_positions, hyperlink_refs):
        hyperlink_cell = None
        for cell in sheet.cells:
            if cell.x == x and cell.y == y:
                hyperlink_cell = cell
                break
        
        assert hyperlink_cell is not None, f"Could not find cell {ref}"
        assert hyperlink_cell.cellformat is not None, f"Cell {ref} lacks formatting information"
        assert hyperlink_cell.cellformat.hyperlink is True, f"Cell {ref} should be hyperlink"
        assert hyperlink_cell.cellformat.is_hyperlink() is True, f"Cell {ref} is_hyperlink() should return True"


def test_xls_non_italic_cell_detection():
    """
    Test that non-italic cells are correctly detected.
    Most cells should not be italic.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C6 (x=2, y=5) which should not be italic
    c6_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 5:
            c6_cell = cell
            break
    
    assert c6_cell is not None, "Could not find cell C6"
    assert c6_cell.cellformat is not None, "Cell C6 lacks formatting information"
    assert c6_cell.cellformat.italic is False, "Cell C6 should not be italic"
    assert c6_cell.cellformat.is_italic() is False, "Cell C6 is_italic() should return False"


def test_xls_non_hyperlink_cell_detection():
    """
    Test that non-hyperlink cells are correctly detected.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C5 (x=2, y=4) which should not be a hyperlink
    c5_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 4:
            c5_cell = cell
            break
    
    assert c5_cell is not None, "Could not find cell C5"
    assert c5_cell.cellformat is not None, "Cell C5 lacks formatting information"
    assert c5_cell.cellformat.hyperlink is False, "Cell C5 should not be hyperlink"
    assert c5_cell.cellformat.is_hyperlink() is False, "Cell C5 is_hyperlink() should return False"


def test_xls_formatting_selection_methods():
    """
    Test that all the formatting selection methods work correctly.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Test bold selection methods
    bold_cells = sheet.is_bold()
    not_bold_cells = sheet.is_not_bold()
    assert len(bold_cells.cells) > 0, "Should find some bold cells"
    assert len(not_bold_cells.cells) > 0, "Should find some non-bold cells"
    assert len(bold_cells.cells) + len(not_bold_cells.cells) == len(sheet.cells), "Bold + not bold should equal total"
    
    # Test italic selection methods
    italic_cells = sheet.is_italic()
    not_italic_cells = sheet.is_not_italic()
    assert len(italic_cells.cells) > 0, "Should find some italic cells"
    assert len(not_italic_cells.cells) > 0, "Should find some non-italic cells"
    assert len(italic_cells.cells) + len(not_italic_cells.cells) == len(sheet.cells), "Italic + not italic should equal total"
    
    # Test underline selection methods
    underline_cells = sheet.is_underline()
    not_underline_cells = sheet.is_not_underline()
    assert len(underline_cells.cells) > 0, "Should find some underlined cells"
    assert len(not_underline_cells.cells) > 0, "Should find some non-underlined cells"
    assert len(underline_cells.cells) + len(not_underline_cells.cells) == len(sheet.cells), "Underline + not underline should equal total"
    
    # Test hyperlink selection methods
    hyperlink_cells = sheet.is_hyperlink()
    not_hyperlink_cells = sheet.is_not_hyperlink()
    assert len(hyperlink_cells.cells) > 0, "Should find some hyperlink cells"
    assert len(not_hyperlink_cells.cells) > 0, "Should find some non-hyperlink cells"
    assert len(hyperlink_cells.cells) + len(not_hyperlink_cells.cells) == len(sheet.cells), "Hyperlink + not hyperlink should equal total"
    
    # Test indentation selection methods
    indented_cells = sheet.is_indented()
    not_indented_cells = sheet.is_not_indented()
    assert len(indented_cells.cells) > 0, "Should find some indented cells"
    assert len(not_indented_cells.cells) > 0, "Should find some non-indented cells"
    assert len(indented_cells.cells) + len(not_indented_cells.cells) == len(sheet.cells), "Indented + not indented should equal total"


def test_xls_indented_cell_detection():
    """
    Test that indented cells are correctly detected.
    Cell C7 (x=2, y=6) in sample.xls should be indented.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C7 (x=2, y=6) which should be indented
    c7_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 6:
            c7_cell = cell
            break
    
    assert c7_cell is not None, "Could not find cell C7"
    assert c7_cell.value == "Office Supply Sales Data", f"Expected 'Office Supply Sales Data', got '{c7_cell.value}'"
    assert c7_cell.cellformat is not None, "Cell C7 lacks formatting information"
    assert c7_cell.cellformat.indent_level > 0, "Cell C7 should have indentation"
    assert c7_cell.cellformat.is_indented() is True, "Cell C7 is_indented() should return True"
    assert c7_cell.cellformat.get_indent_level() == c7_cell.cellformat.indent_level, "get_indent_level() should match indent_level property"


def test_xls_non_indented_cell_detection():
    """
    Test that non-indented cells are correctly detected.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Find cell C5 (x=2, y=4) which should not be indented
    c5_cell = None
    for cell in sheet.cells:
        if cell.x == 2 and cell.y == 4:
            c5_cell = cell
            break
    
    assert c5_cell is not None, "Could not find cell C5"
    assert c5_cell.cellformat is not None, "Cell C5 lacks formatting information"
    assert c5_cell.cellformat.indent_level == 0, "Cell C5 should have no indentation"
    assert c5_cell.cellformat.is_indented() is False, "Cell C5 is_indented() should return False"
    assert c5_cell.cellformat.get_indent_level() == 0, "Cell C5 get_indent_level() should return 0"


def test_xls_specific_indent_level_selection():
    """
    Test that cells can be selected by specific indentation level.
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]
    
    # Test selecting cells with indent level 0 (should be most cells)
    level_0_cells = sheet.has_indent_level(0)
    assert len(level_0_cells.cells) > 0, "Should find cells with indent level 0"
    
    # Test selecting cells with indent level 1 (should find the indented cell)
    level_1_cells = sheet.has_indent_level(1)
    assert len(level_1_cells.cells) > 0, "Should find cells with indent level 1"
    
    # Find the expected indented cell (C7)
    c7_found = False
    for cell in level_1_cells.cells:
        if cell.x == 2 and cell.y == 6:  # C7
            c7_found = True
            break
    assert c7_found, "C7 should be found in indent level 1 selection"
    
    # Test selecting cells with a non-existent indent level
    level_99_cells = sheet.has_indent_level(99)
    assert len(level_99_cells.cells) == 0, "Should find no cells with indent level 99"


def test_unknown_xls_local_time_format_can_be_specified(mocker):
    """
    Test that were we don't have knowledge of an xls time
    format string the user can explicitly pass in a
    formatting string.
    """

    mocker.patch("tidychef.acquire.xls.shared.xls_time_formats", return_value={})

    xls_path: Path = path_to_fixture("xls", "dates-times.xls")
    sheet: XlsSelectable = acquire.xls.local(
        xls_path, tables="Sheet1", custom_time_formats={"DD/MM/YY": "%d/%m/%y"}
    )

    assert [x.value for x in sheet.pcells] == [
        "dates",
        "11/01/23",
        "11/01/23",
        "12/01/22",
        "10/10/00",
    ]
