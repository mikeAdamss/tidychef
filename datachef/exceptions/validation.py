class NoMatcherSpecifiedError(Exception):
    """
    Raised where a user has specified a direct lookup but there is
    not value in the direction specified.
    """

    def __init__(self, msg):
        self.msg = msg
