class FileInputError(Exception):
    """
    There is an issues with what has been provided as a file input.
    """

    def __init__(self, msg: str):
        self.msg = msg


class UnsupportedLocalFileError(Exception):
    """
    User has passed in a local file of a type not currently supported.
    """

    def __init__(self, msg: str):
        self.msg = msg


class UnnamedTableError(Exception):
    """
    User is trying to access the name/title property of a table that does
    not have a name/title property.
    """

    def __init__(self):
        self.msg = (
            "Cannot find table name/title property as this table does not have one. "
            "This is typical of (but not exclusive to) csv tables"
        )


class CellsDoNotExistError(Exception):
    """
    User is trying to select something from the filtered table that
    does not exist in the filtered table.
    """

    def __init__(self, unfound_cells):
        self.msg = f"Requested cells are not in current selection: {unfound_cells}"


class IteratingSingleTableError(Exception):
    """
    User is trying to iterate through an input that consists of
    exactly one table.
    """

    def __init__(self):
        self.msg = (
            "You cannot iterate this input, as it only consists of a single table"
        )


class LoneValueOnMultipleCellsError(Exception):
    """
    Raised when a user attempts to use the Input.long_value() method
    on a selection of more than one cell.
    """

    def __init__(self, number_of_cells: int):
        self.msg = f"You can only use lone_value() on a selection of exactly one cell. This selection has {number_of_cells}"


class InvalidCellObjectError(Exception):
    """
    Raised where a cell object is missing required attributes or
    said attribites hold invalid types or values.
    """

    def __init__(self, msg):
        self.msg = msg


class UnalignedTableOperation(Exception):
    """
    Raised where a user it trying to combine selections from two
    distinct inputs to synthasise a new input.

    This is invalid, as each input represents a subset (up to the whole of)
    a single distinct source of tabulated data.
    """

    def __init__(self):
        self.msg = (
            "Selection can only be combined or previewed in combination"
            "if they are taken from the exact same table as taken from a single "
            "instance of a parsed input."
        )


class InvalidTableSignatures(Exception):
    """
    Raised where someone is constructing a LiveTable from two
    non identical tables.
    """

    def __init__(self):
        self.msg = (
            "This class:LiveTable is invalid. A LiveTable must be "
            "instantiated from tables with matching signatures."
        )


class BadShiftParameterError(Exception):
    """
    Raised where someone has provided incorrect inputs to the
    shift method.
    """

    def __init__(self):
        self.msg = """'
        The shift method must be called with one of two types of
        argument. 

        1.) By passing in the UP, DOWN, LEFT, RIGHT, ABOVE or BELOW constant
        example: .shift(UP)

        2.) By passing in two integer arguments, on each for x index change and y index change
        example: .shift(1, 2)
        """


class OutOfBoundsError(Exception):
    """
    Raised when a users attempts to select cells outside of the
    boundary of the pristine table of input cells.

    Example: Selecting every cell then shifting RIGHT 1 position
    would be trying to select a rightmost column of data that
    does not exist in the table.
    """

    def __init__(self):
        self.msg = "Invalid operation. This action is attempting to select cells outside of the bounds of the input table"
