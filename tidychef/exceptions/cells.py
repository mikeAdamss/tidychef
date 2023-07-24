class NonExistentCellComparissonError(Exception):
    """
    User is trying to to make a positional comparison between an
    existant cell (i.e a cell parsed from a tabulated source) and
    a virtual cell created by a constant or other external input.
    """

    def __init__(self, msg):
        self.msg = msg


class InvlaidCellPositionError(Exception):
    """
    Raised where a cell has a value for one positional index but no the other.

    Examples:
    y has a value but x does not
    x has a value but y does not
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
