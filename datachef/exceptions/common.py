class FileInputError(Exception):
    """
    There is an issues with what has been provided as a file input.
    """

    def __init__(self, msg: str):
        self.msg = msg


class UnnamedTableError(Exception):
    """
    User is trying to access the name/title property of a table that does
    not have a name/title property.
    """

    def __init__(self, msg):
        self.msg = msg


class CellsDoNotExistError(Exception):
    """
    User is trying to select something from the filtered table that
    does not exist in the filtered table.
    """

    def __init__(self, msg):
        self.msg = msg


class LoneValueOnMultipleCellsError(Exception):
    """
    Raised when a user attempts to use the Input.long_value() method
    on a selection of more than one cell.
    """

    def __init__(self, msg):
        self.msg = msg


class InvalidCellObjectError(Exception):
    """
    Raised where a cell object is missing required attributes or
    said attributes hold invalid types or values.
    """

    def __init__(self, msg):
        self.msg = msg


class UnalignedTableOperation(Exception):
    """
    Raised where a user it trying to combine cell selections from two
    distinctly separate inputs.

    This is invalid, as each input represents a subset (up to the whole of)
    a single distinct source of tabulated data.
    """

    def __init__(self, msg):
        self.msg = msg


class InvalidTableSignatures(Exception):
    """
    Raised where someone is constructing a LiveTable from two
    non identical tables.
    """

    def __init__(self, msg):
        self.msg = msg


class OutOfBoundsError(Exception):
    """
    Raised when a users attempts to select or reference a cell
    outside of the boundary of the pristine table of input cells.

    Example: Selecting every cell then shifting RIGHT 1 position
    would be trying to select a rightmost column of data that
    does not exist in the table.
    """

    def __init__(self, msg):
        self.msg = msg


class ImpossibleLookupError(Exception):
    """
    Raised when a user is attempting a lookup that is impossible
    to resolve.

    For example: looming up to a cell that is "above" directionally
    when no cells in the direction have been selected.
    """

    def __init__(self, msg):
        self.msg = msg


class MissingLabelError(Exception):
    """
    Raised where a user is trying to construct an output with a
    selection of cells but has not yet labelled that selection of
    cells
    """

    def __init__(self, msg):
        self.msg = msg


class BadConditionalResolverError(Exception):
    """
    Raised where a user has specified a HorizontalCondition
    lookup engine that has incorrect arguments or returns
    as incorrect types.
    """

    def __init__(self, msg):
        self.msg = msg


class HorizontalConditionalHeaderError(Exception):
    """
    Raised where a user has specified a HorizontalCondition
    lookup engine but its failing to resolve as an expected
    column value is missing.
    """

    def __init__(self, msg):
        self.msg = msg


class PreviewBoundarySpecificationError(Exception):
    """
    Raised where a user is trying to create a preview with a
    set boundary but has provided incorrect parameters.
    """

    def __init__(self, msg):
        self.msg = msg


class MisalignedHeadersError(Exception):
    """
    Raised where a user is attempting to join together two
    TidyData outputs but those outputs do not have the
    same column headers.
    """

    def __init__(self, msg):
        self.msg = msg


class CellValidationError(Exception):
    """
    Raised where we're validated a call value and
    found it to me invalid.
    """

    def __init__(self, msg):
        self.msg = msg

class DroppingNonColumnError(Exception):
    """
    Raised where a user is trying to drop a column
    during the transformation to tidy data but that
    column does not exist.
    """

    def __init__(self, msg):
        self.msg = msg