class AmbiguousLookupError(Exception):
    """
    Raised where a user has configured a lookup engine such that it
    cannot concretely resolve a lookup against one of more observation
    cells.
    """

    def __init__(self, msg):
        self.msg = msg


class MissingDirectLookupError(Exception):
    """
    Raised where a user has specified a direct lookup but there is
    not value in the direction specified.
    """

    def __init__(self, msg):
        self.msg = msg


class FailedLookupError(Exception):
    """
    Raised where a lookup engine fails to resolve a result cell
    """

    def __init__(self, msg):
        self.msg = msg
