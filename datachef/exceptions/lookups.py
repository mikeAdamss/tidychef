
class MissingDirectLookupError(Exception):
    """
    Raised where a user has specified a direct lookup but there is
    not value in the direction specified.
    """

    def __init__(
        self, msg=("Cannot use a direct lookup, no value found in the direction specified"), *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)

class FailedLookupError(Exception):
    """
    Raised where a lookup engine fails to resolve a result cell
    """

    def __init__(
        self, msg=("Lookup has failed, no relative cell could be resolved."), *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)