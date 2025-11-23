from dataclasses import dataclass
from typing import Optional

from tidychef.exceptions import CellFormattingError


@dataclass
class CellFormatting:
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    hyperlink: Optional[bool] = None
    indent_level: Optional[int] = None
    horizontal_alignment: Optional[str] = None  # 'left', 'center', 'right', 'justify', 'general'
    vertical_alignment: Optional[str] = None  # 'top', 'center', 'bottom'
    
    def is_bold(self) -> bool:
        """
        Check if the cell is bold.
        
        Returns:
            bool: True if cell is bold, False if not bold
            
        Raises:
            CellFormattingError: If bold formatting state is unknown (None)
        """
        if self.bold is None:
            raise CellFormattingError(
                "Bold formatting state is unknown. Cannot determine if cell is bold."
            )
        return self.bold
    
    def is_italic(self) -> bool:
        """
        Check if the cell is italic.
        
        Returns:
            bool: True if cell is italic, False if not italic
            
        Raises:
            CellFormattingError: If italic formatting state is unknown (None)
        """
        if self.italic is None:
            raise CellFormattingError(
                "Italic formatting state is unknown. Cannot determine if cell is italic."
            )
        return self.italic
    
    def is_underline(self) -> bool:
        """
        Check if the cell is underlined.
        
        Returns:
            bool: True if cell is underlined, False if not underlined
            
        Raises:
            CellFormattingError: If underline formatting state is unknown (None)
        """
        if self.underline is None:
            raise CellFormattingError(
                "Underline formatting state is unknown. Cannot determine if cell is underlined."
            )
        return self.underline
    
    def is_hyperlink(self) -> bool:
        """
        Check if the cell is a hyperlink.
        
        Returns:
            bool: True if cell is a hyperlink, False if not a hyperlink
            
        Raises:
            CellFormattingError: If hyperlink formatting state is unknown (None)
        """
        if self.hyperlink is None:
            raise CellFormattingError(
                "Hyperlink formatting state is unknown. Cannot determine if cell is a hyperlink."
            )
        return self.hyperlink
    
    def get_indent_level(self) -> int:
        """
        Get the indentation level of the cell.
        
        Returns:
            int: The indentation level (0 = no indentation)
            
        Raises:
            CellFormattingError: If indentation level is unknown (None)
        """
        if self.indent_level is None:
            raise CellFormattingError(
                "Indentation level is unknown. Cannot determine cell indentation."
            )
        return self.indent_level
    
    def is_indented(self) -> bool:
        """
        Check if the cell has any indentation.
        
        Returns:
            bool: True if cell has indentation (indent_level > 0), False otherwise
            
        Raises:
            CellFormattingError: If indentation level is unknown (None)
        """
        if self.indent_level is None:
            raise CellFormattingError(
                "Indentation level is unknown. Cannot determine if cell is indented."
            )
        return self.indent_level > 0
    
    def get_horizontal_alignment(self) -> str:
        """
        Get the horizontal alignment of the cell.
        
        Returns:
            str: The horizontal alignment ('left', 'center', 'right', 'justify', 'general')
                 Returns 'general' if alignment is not specified (Excel default behavior)
        """
        return self.horizontal_alignment or 'general'
    
    def get_vertical_alignment(self) -> str:
        """
        Get the vertical alignment of the cell.
        
        Returns:
            str: The vertical alignment ('top', 'center', 'bottom')
                 Returns 'bottom' if alignment is not specified (Excel default behavior)
        """
        return self.vertical_alignment or 'bottom'
    
    def is_left_aligned(self) -> bool:
        """
        Check if the cell is left-aligned.
        
        Returns:
            bool: True if cell is explicitly left-aligned, False otherwise
        """
        return self.horizontal_alignment == 'left'
    
    def is_center_aligned(self) -> bool:
        """
        Check if the cell is center-aligned.
        
        Returns:
            bool: True if cell is center-aligned, False otherwise
        """
        return self.horizontal_alignment == 'center'
    
    def is_right_aligned(self) -> bool:
        """
        Check if the cell is right-aligned.
        
        Returns:
            bool: True if cell is right-aligned, False otherwise
        """
        return self.horizontal_alignment == 'right'
