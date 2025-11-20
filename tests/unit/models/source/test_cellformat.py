import pytest

from tidychef.exceptions import CellFormattingError
from tidychef.models.source.cellformat import CellFormatting


class TestCellFormatting:
    """Test cases for the CellFormatting class."""

    def test_cellformatting_default_initialization(self):
        """Test that CellFormatting initializes with default values."""
        cell_format = CellFormatting()
        assert cell_format.bold is None
        assert cell_format.italic is None
        assert cell_format.underline is None
        assert cell_format.hyperlink is None
        assert cell_format.indent_level is None

    def test_cellformatting_initialization_with_bold_true(self):
        """Test that CellFormatting can be initialized with bold=True."""
        cell_format = CellFormatting(bold=True)
        assert cell_format.bold is True

    def test_cellformatting_initialization_with_bold_false(self):
        """Test that CellFormatting can be initialized with bold=False."""
        cell_format = CellFormatting(bold=False)
        assert cell_format.bold is False

    def test_cellformatting_initialization_with_bold_none(self):
        """Test that CellFormatting can be initialized with bold=None."""
        cell_format = CellFormatting(bold=None)
        assert cell_format.bold is None

    def test_is_bold_returns_true_when_bold_is_true(self):
        """Test that is_bold() returns True when bold attribute is True."""
        cell_format = CellFormatting(bold=True)
        assert cell_format.is_bold() is True

    def test_is_bold_returns_false_when_bold_is_false(self):
        """Test that is_bold() returns False when bold attribute is False."""
        cell_format = CellFormatting(bold=False)
        assert cell_format.is_bold() is False

    def test_is_bold_raises_cellformattingerror_when_bold_is_none(self):
        """Test that is_bold() raises CellFormattingError when bold is None."""
        cell_format = CellFormatting(bold=None)
        
        with pytest.raises(CellFormattingError) as exc_info:
            cell_format.is_bold()
        
        assert "Bold formatting state is unknown" in exc_info.value.msg

    def test_is_bold_exception_message_content(self):
        """Test that the exception message contains expected content."""
        cell_format = CellFormatting()
        
        with pytest.raises(CellFormattingError) as exc_info:
            cell_format.is_bold()
        
        expected_message = "Bold formatting state is unknown. Cannot determine if cell is bold."
        assert exc_info.value.msg == expected_message

    def test_cellformatting_dataclass_equality(self):
        """Test that CellFormatting instances with same values are equal."""
        cell_format1 = CellFormatting(bold=True)
        cell_format2 = CellFormatting(bold=True)
        cell_format3 = CellFormatting(bold=False)
        
        assert cell_format1 == cell_format2
        assert cell_format1 != cell_format3

    def test_cellformatting_dataclass_repr(self):
        """Test that CellFormatting has proper string representation."""
        cell_format = CellFormatting(bold=True)
        repr_str = repr(cell_format)
        
        assert "CellFormatting" in repr_str
        assert "bold=True" in repr_str

    # Italic formatting tests
    def test_cellformatting_initialization_with_italic_true(self):
        """Test that CellFormatting can be initialized with italic=True."""
        cell_format = CellFormatting(italic=True)
        assert cell_format.italic is True

    def test_cellformatting_initialization_with_italic_false(self):
        """Test that CellFormatting can be initialized with italic=False."""
        cell_format = CellFormatting(italic=False)
        assert cell_format.italic is False

    def test_is_italic_returns_true_when_italic_is_true(self):
        """Test that is_italic() returns True when italic attribute is True."""
        cell_format = CellFormatting(italic=True)
        assert cell_format.is_italic() is True

    def test_is_italic_returns_false_when_italic_is_false(self):
        """Test that is_italic() returns False when italic attribute is False."""
        cell_format = CellFormatting(italic=False)
        assert cell_format.is_italic() is False

    def test_is_italic_raises_cellformattingerror_when_italic_is_none(self):
        """Test that is_italic() raises CellFormattingError when italic is None."""
        cell_format = CellFormatting(italic=None)
        
        with pytest.raises(CellFormattingError) as exc_info:
            cell_format.is_italic()
        
        assert "Italic formatting state is unknown" in exc_info.value.msg

    # Underline formatting tests
    def test_cellformatting_initialization_with_underline_true(self):
        """Test that CellFormatting can be initialized with underline=True."""
        cell_format = CellFormatting(underline=True)
        assert cell_format.underline is True

    def test_cellformatting_initialization_with_underline_false(self):
        """Test that CellFormatting can be initialized with underline=False."""
        cell_format = CellFormatting(underline=False)
        assert cell_format.underline is False

    def test_is_underline_returns_true_when_underline_is_true(self):
        """Test that is_underline() returns True when underline attribute is True."""
        cell_format = CellFormatting(underline=True)
        assert cell_format.is_underline() is True

    def test_is_underline_returns_false_when_underline_is_false(self):
        """Test that is_underline() returns False when underline attribute is False."""
        cell_format = CellFormatting(underline=False)
        assert cell_format.is_underline() is False

    def test_is_underline_raises_cellformattingerror_when_underline_is_none(self):
        """Test that is_underline() raises CellFormattingError when underline is None."""
        cell_format = CellFormatting(underline=None)
        
        with pytest.raises(CellFormattingError) as exc_info:
            cell_format.is_underline()
        
        assert "Underline formatting state is unknown" in exc_info.value.msg

    # Hyperlink formatting tests
    def test_cellformatting_initialization_with_hyperlink_true(self):
        """Test that CellFormatting can be initialized with hyperlink=True."""
        cell_format = CellFormatting(hyperlink=True)
        assert cell_format.hyperlink is True

    def test_cellformatting_initialization_with_hyperlink_false(self):
        """Test that CellFormatting can be initialized with hyperlink=False."""
        cell_format = CellFormatting(hyperlink=False)
        assert cell_format.hyperlink is False

    def test_is_hyperlink_returns_true_when_hyperlink_is_true(self):
        """Test that is_hyperlink() returns True when hyperlink attribute is True."""
        cell_format = CellFormatting(hyperlink=True)
        assert cell_format.is_hyperlink() is True

    def test_is_hyperlink_returns_false_when_hyperlink_is_false(self):
        """Test that is_hyperlink() returns False when hyperlink attribute is False."""
        cell_format = CellFormatting(hyperlink=False)
        assert cell_format.is_hyperlink() is False

    def test_is_hyperlink_raises_cellformattingerror_when_hyperlink_is_none(self):
        """Test that is_hyperlink() raises CellFormattingError when hyperlink is None."""
        cell_format = CellFormatting(hyperlink=None)
        
        with pytest.raises(CellFormattingError) as exc_info:
            cell_format.is_hyperlink()
        
        assert "Hyperlink formatting state is unknown" in exc_info.value.msg

    # Indentation tests
    def test_cellformatting_initialization_with_indent_level_zero(self):
        """Test that CellFormatting can be initialized with indent_level=0."""
        cell_format = CellFormatting(indent_level=0)
        assert cell_format.indent_level == 0

    def test_cellformatting_initialization_with_indent_level_positive(self):
        """Test that CellFormatting can be initialized with positive indent_level."""
        cell_format = CellFormatting(indent_level=3)
        assert cell_format.indent_level == 3

    def test_get_indent_level_returns_correct_level(self):
        """Test that get_indent_level() returns the correct indentation level."""
        cell_format = CellFormatting(indent_level=2)
        assert cell_format.get_indent_level() == 2

    def test_get_indent_level_raises_cellformattingerror_when_indent_level_is_none(self):
        """Test that get_indent_level() raises CellFormattingError when indent_level is None."""
        cell_format = CellFormatting(indent_level=None)
        
        with pytest.raises(CellFormattingError) as exc_info:
            cell_format.get_indent_level()
        
        assert "Indentation level is unknown" in exc_info.value.msg

    def test_is_indented_returns_true_when_indent_level_greater_than_zero(self):
        """Test that is_indented() returns True when indent_level > 0."""
        cell_format = CellFormatting(indent_level=1)
        assert cell_format.is_indented() is True

    def test_is_indented_returns_false_when_indent_level_is_zero(self):
        """Test that is_indented() returns False when indent_level is 0."""
        cell_format = CellFormatting(indent_level=0)
        assert cell_format.is_indented() is False

    def test_is_indented_raises_cellformattingerror_when_indent_level_is_none(self):
        """Test that is_indented() raises CellFormattingError when indent_level is None."""
        cell_format = CellFormatting(indent_level=None)
        
        with pytest.raises(CellFormattingError) as exc_info:
            cell_format.is_indented()
        
        assert "Indentation level is unknown" in exc_info.value.msg

    # Complete initialization test
    def test_cellformatting_initialization_with_all_properties(self):
        """Test that CellFormatting can be initialized with all properties."""
        cell_format = CellFormatting(
            bold=True,
            italic=False,
            underline=True,
            hyperlink=False,
            indent_level=2
        )
        assert cell_format.bold is True
        assert cell_format.italic is False
        assert cell_format.underline is True
        assert cell_format.hyperlink is False
        assert cell_format.indent_level == 2

    def test_cellformatting_dataclass_equality_with_all_properties(self):
        """Test that CellFormatting instances with same values are equal including all properties."""
        cell_format1 = CellFormatting(bold=True, italic=False, underline=True, hyperlink=False, indent_level=1)
        cell_format2 = CellFormatting(bold=True, italic=False, underline=True, hyperlink=False, indent_level=1)
        cell_format3 = CellFormatting(bold=False, italic=False, underline=True, hyperlink=False, indent_level=1)
        
        assert cell_format1 == cell_format2
        assert cell_format1 != cell_format3

    def test_cellformatting_dataclass_repr_with_multiple_properties(self):
        """Test that CellFormatting has proper string representation with multiple properties."""
        cell_format = CellFormatting(bold=True, italic=False, indent_level=2)
        repr_str = repr(cell_format)
        
        assert "CellFormatting" in repr_str
        assert "bold=True" in repr_str
        assert "italic=False" in repr_str
        assert "indent_level=2" in repr_str


class TestCellFormattingErrorHandling:
    """Test cases specifically for error handling scenarios."""

    def test_cellformattingerror_is_catchable(self):
        """Test that CellFormattingError can be caught and handled."""
        cell_format = CellFormatting(bold=None)
        
        try:
            cell_format.is_bold()
            # Should not reach this line
            assert False, "Expected CellFormattingError was not raised"
        except CellFormattingError as e:
            # Should catch the exception successfully
            assert e.msg is not None
            assert len(e.msg) > 0

    def test_cellformattingerror_does_not_catch_other_errors(self):
        """Test that catching CellFormattingError doesn't catch other exceptions."""
        cell_format = CellFormatting(bold=True)
        
        # This should not raise CellFormattingError, so the except block shouldn't execute
        caught_formatting_error = False
        try:
            result = cell_format.is_bold()  # Should return True, not raise an error
            assert result is True
        except CellFormattingError:
            caught_formatting_error = True
        
        assert not caught_formatting_error

    def test_multiple_cellformatting_instances_with_none_all_raise_error(self):
        """Test that multiple CellFormatting instances with None bold all raise errors."""
        instances = [CellFormatting() for _ in range(3)]
        
        for i, cell_format in enumerate(instances):
            with pytest.raises(CellFormattingError):
                cell_format.is_bold()
