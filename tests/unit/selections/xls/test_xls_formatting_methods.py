from unittest.mock import Mock

import pytest

from tidychef.exceptions import CellFormattingError
from tidychef.models.source.cellformat import CellFormatting
from tidychef.models.source.table import Table
from tidychef.selection.xls.xls import XlsSelectable


class TestXlsSelectableItalicMethods:
    """Test cases for XlsSelectable italic filtering methods."""

    def setup_method(self):
        """Set up test fixtures."""
        self.italic_cell = Mock()
        self.italic_cell.cellformat = CellFormatting(italic=True)
        self.italic_cell.x, self.italic_cell.y = 0, 0
        
        self.not_italic_cell = Mock()
        self.not_italic_cell.cellformat = CellFormatting(italic=False)
        self.not_italic_cell.x, self.not_italic_cell.y = 1, 0
        
        self.unknown_italic_cell = Mock()
        self.unknown_italic_cell.cellformat = CellFormatting(italic=None)
        self.unknown_italic_cell._excel_ref = Mock(return_value="C3")
        self.unknown_italic_cell.x, self.unknown_italic_cell.y = 2, 0

    def test_is_italic_filters_correctly(self):
        """Test that is_italic() filters to only italic cells."""
        data_table = Table()
        data_table.cells = [self.italic_cell, self.not_italic_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_italic()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.italic is True

    def test_is_not_italic_filters_correctly(self):
        """Test that is_not_italic() filters to only non-italic cells."""
        data_table = Table()
        data_table.cells = [self.italic_cell, self.not_italic_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_not_italic()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.italic is False

    def test_is_italic_raises_error_on_unknown_formatting(self):
        """Test that is_italic() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_italic_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_italic()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg

    def test_is_not_italic_raises_error_on_unknown_formatting(self):
        """Test that is_not_italic() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_italic_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_not_italic()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg


class TestXlsSelectableUnderlineMethods:
    """Test cases for XlsSelectable underline filtering methods."""

    def setup_method(self):
        """Set up test fixtures."""
        self.underline_cell = Mock()
        self.underline_cell.cellformat = CellFormatting(underline=True, hyperlink=False)
        self.underline_cell.x, self.underline_cell.y = 0, 0
        
        self.not_underline_cell = Mock()
        self.not_underline_cell.cellformat = CellFormatting(underline=False, hyperlink=False)
        self.not_underline_cell.x, self.not_underline_cell.y = 1, 0
        
        self.hyperlink_cell = Mock()
        self.hyperlink_cell.cellformat = CellFormatting(underline=True, hyperlink=True)
        self.hyperlink_cell.x, self.hyperlink_cell.y = 2, 0
        
        self.unknown_underline_cell = Mock()
        self.unknown_underline_cell.cellformat = CellFormatting(underline=None, hyperlink=False)
        self.unknown_underline_cell._excel_ref = Mock(return_value="D4")
        self.unknown_underline_cell.x, self.unknown_underline_cell.y = 3, 0

    def test_is_underline_filters_correctly_default_excludes_hyperlinks(self):
        """Test that is_underline() by default excludes hyperlinks and only returns decoratively underlined cells."""
        data_table = Table()
        data_table.cells = [self.underline_cell, self.not_underline_cell, self.hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_underline()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.underline is True
        assert result.cells[0].cellformat.hyperlink is False

    def test_is_underline_with_include_hyperlinks_true(self):
        """Test that is_underline(include_hyperlinks=True) includes both decorative underlines and hyperlinks."""
        data_table = Table()
        data_table.cells = [self.underline_cell, self.not_underline_cell, self.hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_underline(include_hyperlinks=True)
        assert len(result.cells) == 2
        # Should include both the decoratively underlined cell and the hyperlink
        underlined_cells = [cell for cell in result.cells if cell.cellformat.underline]
        assert len(underlined_cells) == 2

    def test_is_underline_with_include_hyperlinks_false_explicit(self):
        """Test that is_underline(include_hyperlinks=False) explicitly excludes hyperlinks."""
        data_table = Table()
        data_table.cells = [self.underline_cell, self.not_underline_cell, self.hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_underline(include_hyperlinks=False)
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.underline is True
        assert result.cells[0].cellformat.hyperlink is False

    def test_is_not_underline_filters_correctly(self):
        """Test that is_not_underline() filters to only non-underlined cells."""
        data_table = Table()
        data_table.cells = [self.underline_cell, self.not_underline_cell, self.hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_not_underline()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.underline is False

    def test_is_underline_raises_error_on_unknown_formatting(self):
        """Test that is_underline() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_underline_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_underline()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg

    def test_is_not_underline_raises_error_on_unknown_formatting(self):
        """Test that is_not_underline() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_underline_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_not_underline()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg


class TestXlsSelectableHyperlinkMethods:
    """Test cases for XlsSelectable hyperlink filtering methods."""

    def setup_method(self):
        """Set up test fixtures."""
        self.hyperlink_cell = Mock()
        self.hyperlink_cell.cellformat = CellFormatting(hyperlink=True)
        self.hyperlink_cell.x, self.hyperlink_cell.y = 0, 0
        
        self.not_hyperlink_cell = Mock()
        self.not_hyperlink_cell.cellformat = CellFormatting(hyperlink=False)
        self.not_hyperlink_cell.x, self.not_hyperlink_cell.y = 1, 0
        
        self.unknown_hyperlink_cell = Mock()
        self.unknown_hyperlink_cell.cellformat = CellFormatting(hyperlink=None)
        self.unknown_hyperlink_cell._excel_ref = Mock(return_value="E5")
        self.unknown_hyperlink_cell.x, self.unknown_hyperlink_cell.y = 2, 0

    def test_is_hyperlink_filters_correctly(self):
        """Test that is_hyperlink() filters to only hyperlink cells."""
        data_table = Table()
        data_table.cells = [self.hyperlink_cell, self.not_hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_hyperlink()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.hyperlink is True

    def test_is_not_hyperlink_filters_correctly(self):
        """Test that is_not_hyperlink() filters to only non-hyperlink cells."""
        data_table = Table()
        data_table.cells = [self.hyperlink_cell, self.not_hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_not_hyperlink()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.hyperlink is False

    def test_is_hyperlink_raises_error_on_unknown_formatting(self):
        """Test that is_hyperlink() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_hyperlink()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg

    def test_is_not_hyperlink_raises_error_on_unknown_formatting(self):
        """Test that is_not_hyperlink() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_hyperlink_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_not_hyperlink()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg


class TestXlsSelectableIndentationMethods:
    """Test cases for XlsSelectable indentation filtering methods."""

    def setup_method(self):
        """Set up test fixtures."""
        self.indented_cell = Mock()
        self.indented_cell.cellformat = CellFormatting(indent_level=1)
        self.indented_cell.x, self.indented_cell.y = 0, 0
        
        self.not_indented_cell = Mock()
        self.not_indented_cell.cellformat = CellFormatting(indent_level=0)
        self.not_indented_cell.x, self.not_indented_cell.y = 1, 0
        
        self.unknown_indent_cell = Mock()
        self.unknown_indent_cell.cellformat = CellFormatting(indent_level=None)
        self.unknown_indent_cell._excel_ref = Mock(return_value="F6")
        self.unknown_indent_cell.x, self.unknown_indent_cell.y = 2, 0

    def test_is_indented_filters_correctly(self):
        """Test that is_indented() filters to only indented cells."""
        data_table = Table()
        data_table.cells = [self.indented_cell, self.not_indented_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_indented()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.indent_level > 0

    def test_is_not_indented_filters_correctly(self):
        """Test that is_not_indented() filters to only non-indented cells."""
        data_table = Table()
        data_table.cells = [self.indented_cell, self.not_indented_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.is_not_indented()
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.indent_level == 0

    def test_has_indent_level_filters_correctly(self):
        """Test that has_indent_level() filters to cells with specific indent level."""
        data_table = Table()
        data_table.cells = [self.indented_cell, self.not_indented_cell]
        selectable = XlsSelectable(data_table)
        
        result = selectable.has_indent_level(1)
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.indent_level == 1

    def test_is_indented_raises_error_on_unknown_formatting(self):
        """Test that is_indented() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_indent_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_indented()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg

    def test_is_not_indented_raises_error_on_unknown_formatting(self):
        """Test that is_not_indented() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_indent_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_not_indented()
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg

    def test_has_indent_level_raises_error_on_unknown_formatting(self):
        """Test that has_indent_level() raises CellFormattingError when encountering unknown formatting."""
        data_table = Table()
        data_table.cells = [self.unknown_indent_cell]
        selectable = XlsSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.has_indent_level(0)
        
        assert "Unexpected formatting error for XLS cell" in exc_info.value.msg
