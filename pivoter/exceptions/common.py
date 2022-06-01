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
