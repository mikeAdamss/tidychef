from ..selectable import Selectable
from tidychef.exceptions import CellFormattingError
from tidychef.utils.decorators import dontmutate


class XlsxSelectable(Selectable):
    """
    Class representing an Xlsx input
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
                # This should not happen in normal XLSX processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLSX cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
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
                # This should not happen in normal XLSX processing as cells should have
                # proper formatting information. Re-raise to indicate a serious issue.
                raise CellFormattingError(
                    f"Unexpected formatting error for XLSX cell at {cell._excel_ref() if hasattr(cell, '_excel_ref') else 'unknown position'}: {e.msg}"
                ) from e
        
        self.cells = filtered_cells
        return self
