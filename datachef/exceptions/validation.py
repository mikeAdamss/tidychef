class NoMatcherSpecifiedError(Exception):
    """
    Raised where a user has specified a direct lookup but there is
    not value in the direction specified.
    """

    def __init__(self):
        self.msg = """
                You are passing a cell to a Matcher that has not
                been configured with a matching strategy.

                Examples of correct usage:

                match.regex("foo")
                match.one_of("foo", "bar", "baz")
            """
