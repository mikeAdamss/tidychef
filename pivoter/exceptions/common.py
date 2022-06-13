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


class OutOfBoundsError(Exception):
    """
    User is trying to select something from the filtred table that
    does not exist in the filtered table.
    """

    def __init__(self, msg: str):
        self.msg = msg


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
