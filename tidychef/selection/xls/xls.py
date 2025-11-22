from tidychef.exceptions import CellFormattingError
from tidychef.utils.decorators import dontmutate

from ..selectable import Selectable


class XlsSelectable(Selectable):
    """
    Class representing an Xls input
    """

    @dontmutate
    def is_bold(self):
        """
        Filters the selection to those cells that are bold.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if cell.cellformat.is_bold():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_indented(self):
        """
        Filters the selection to those cells that are indented (indent_level > 0).
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if cell.cellformat.is_indented():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_not_indented(self):
        """
        Filters the selection to those cells that are not indented (indent_level == 0).
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if not cell.cellformat.is_indented():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def has_indent_level(self, level: int):
        """
        Filters the selection to those cells that have a specific indentation level.
        
        Args:
            level (int): The specific indentation level to filter by
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if cell.cellformat.get_indent_level() == level:
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_italic(self):
        """
        Filters the selection to those cells that are italic.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if cell.cellformat.is_italic():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_not_italic(self):
        """
        Filters the selection to those cells that are not italic.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if not cell.cellformat.is_italic():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_underline(self, include_hyperlinks: bool = False):
        """
        Filters the selection to those cells that are underlined.
        
        Args:
            include_hyperlinks (bool): If False (default), excludes hyperlinks from the selection 
                                     to focus on decoratively underlined text. If True, includes 
                                     all underlined cells including hyperlinks.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                is_underlined = cell.cellformat.is_underline()
                is_hyperlink = cell.cellformat.is_hyperlink()
                
                # Include cell if it's underlined and either:
                # - We're including hyperlinks, OR
                # - It's not a hyperlink (decorative underline only)
                if is_underlined and (include_hyperlinks or not is_hyperlink):
                    filtered_cells.append(cell)
                    
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_not_underline(self):
        """
        Filters the selection to those cells that are not underlined.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if not cell.cellformat.is_underline():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_hyperlink(self):
        """
        Filters the selection to those cells that are hyperlinks.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if cell.cellformat.is_hyperlink():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_not_hyperlink(self):
        """
        Filters the selection to those cells that are not hyperlinks.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if not cell.cellformat.is_hyperlink():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self

    @dontmutate
    def is_not_bold(self):
        """
        Filters the selection to those cells that are not bold.
        """
        filtered_cells = []
        for cell in self.cells:
            try:
                if not cell.cellformat.is_bold():
                    filtered_cells.append(cell)
            except CellFormattingError as e:
                # This should not happen in normal XLS processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLS cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self
