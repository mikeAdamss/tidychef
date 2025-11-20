import pytest
from unittest.mock import Mock, patch

from tidychef.exceptions import CellFormattingError
from tidychef.models.source.cellformat import CellFormatting
from tidychef.models.source.table import Table
from tidychef.selection.xlsx.xlsx import XlsxSelectable


class TestXlsxSelectableBoldMethods:
    """Test cases for XlsxSelectable bold filtering methods."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create mock cells with different bold states
        self.bold_cell = Mock()
        self.bold_cell.cellformat = CellFormatting(bold=True)
        self.bold_cell.x = 0  # Add coordinate attributes for neighbor graph
        self.bold_cell.y = 0
        
        self.not_bold_cell = Mock()
        self.not_bold_cell.cellformat = CellFormatting(bold=False)
        self.not_bold_cell.x = 1  # Different coordinates to avoid conflicts
        self.not_bold_cell.y = 0
        
        self.unknown_bold_cell = Mock()
        self.unknown_bold_cell.cellformat = CellFormatting(bold=None)
        self.unknown_bold_cell._excel_ref = Mock(return_value="A1")
        self.unknown_bold_cell.x = 2  # Different coordinates
        self.unknown_bold_cell.y = 0

    def test_is_bold_filters_to_bold_cells_only(self):
        """Test that is_bold() filters to only bold cells."""
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = [self.bold_cell, self.not_bold_cell]
        selectable = XlsxSelectable(data_table)
        
        # Call the method
        result = selectable.is_bold()
        
        # Should only contain the bold cell
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.bold is True
        assert result is not selectable  # @dontmutate creates a new instance

    def test_is_not_bold_filters_to_non_bold_cells_only(self):
        """Test that is_not_bold() filters to only non-bold cells."""
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = [self.bold_cell, self.not_bold_cell]
        selectable = XlsxSelectable(data_table)
        
        # Call the method
        result = selectable.is_not_bold()
        
        # Should only contain the not bold cell
        assert len(result.cells) == 1
        assert result.cells[0].cellformat.bold is False
        assert result is not selectable  # @dontmutate creates a new instance

    def test_is_bold_raises_error_on_unknown_formatting(self):
        """Test that is_bold() raises CellFormattingError when encountering unknown formatting."""
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = [self.unknown_bold_cell]
        selectable = XlsxSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_bold()
        
        # Should contain information about the unexpected error
        assert "Unexpected formatting error for XLSX cell" in exc_info.value.msg
        assert "A1" in exc_info.value.msg

    def test_is_not_bold_raises_error_on_unknown_formatting(self):
        """Test that is_not_bold() raises CellFormattingError when encountering unknown formatting."""
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = [self.unknown_bold_cell]
        selectable = XlsxSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_not_bold()
        
        # Should contain information about the unexpected error
        assert "Unexpected formatting error for XLSX cell" in exc_info.value.msg
        assert "A1" in exc_info.value.msg

    def test_is_bold_with_mixed_cells(self):
        """Test is_bold() with a mix of bold and not bold cells."""
        # Add another bold cell
        another_bold_cell = Mock()
        another_bold_cell.cellformat = CellFormatting(bold=True)
        another_bold_cell.x = 3  # Different coordinates
        another_bold_cell.y = 0
        
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = [
            self.bold_cell, 
            self.not_bold_cell, 
            another_bold_cell
        ]
        selectable = XlsxSelectable(data_table)
        
        result = selectable.is_bold()
        
        # Should contain both bold cells
        assert len(result.cells) == 2
        bold_cells = [cell for cell in result.cells if cell.cellformat.bold is True]
        assert len(bold_cells) == 2
        assert result is not selectable  # @dontmutate creates a new instance

    def test_is_not_bold_with_mixed_cells(self):
        """Test is_not_bold() with a mix of bold and not bold cells."""
        # Add another not bold cell
        another_not_bold_cell = Mock()
        another_not_bold_cell.cellformat = CellFormatting(bold=False)
        another_not_bold_cell.x = 4  # Different coordinates
        another_not_bold_cell.y = 0
        
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = [
            self.bold_cell, 
            self.not_bold_cell, 
            another_not_bold_cell
        ]
        selectable = XlsxSelectable(data_table)
        
        result = selectable.is_not_bold()
        
        # Should contain both not bold cells
        assert len(result.cells) == 2
        not_bold_cells = [cell for cell in result.cells if cell.cellformat.bold is False]
        assert len(not_bold_cells) == 2
        assert result is not selectable  # @dontmutate creates a new instance

    def test_is_bold_with_empty_selection(self):
        """Test is_bold() with empty cell selection."""
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = []
        selectable = XlsxSelectable(data_table)
        
        result = selectable.is_bold()
        
        assert len(result.cells) == 0
        assert result is not selectable  # @dontmutate creates a new instance

    def test_is_not_bold_with_empty_selection(self):
        """Test is_not_bold() with empty cell selection."""
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = []
        selectable = XlsxSelectable(data_table)
        
        result = selectable.is_not_bold()
        
        assert len(result.cells) == 0
        assert result is not selectable  # @dontmutate creates a new instance

    def test_error_handling_preserves_original_exception_chain(self):
        """Test that error handling preserves the original exception chain."""
        # Create a real Table instance instead of Mock
        data_table = Table()
        data_table.cells = [self.unknown_bold_cell]
        selectable = XlsxSelectable(data_table)
        
        with pytest.raises(CellFormattingError) as exc_info:
            selectable.is_bold()
        
        # Should have the original exception as the cause
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, CellFormattingError)
