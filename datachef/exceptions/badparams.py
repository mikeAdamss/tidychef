from os import linesep


class BadExcelReferenceError(Exception):
    """
    Raised where the user has provided an excel reference that does not match
    the known patterns for excel references.
    """

    def __init__(
        self, msg=("Could not understand the provided excel reference"), *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class BadShiftParameterError(Exception):
    """
    Raised where someone has provided incorrect inputs to the
    shift method.
    """

    def __init__(
        self,
        msg=(
            f"The shift method must be called with one of two types of argument{linesep}"
            f"1.) By passing in an up, down, left, right, above or below direction, "
            f"for example: .shift(up). {linesep}"
            "2.) By passing in two integer arguments, on each for x index change and y index change"
            "example: .shift(1, 2)"
        ),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


class CardinalDeclarationWithOffset(Exception):
    def __init__(self, msg):
        self.msg = msg


class WithinAxisDeclarationError(Exception):
    """
    Raised where a user is attempting a within lookup but is
    mixing axis.

    i.e we must be scanning between two directions along a
    single axis, eg:

    - left to right
    - up to down
    - below to above
    etc

    We cannot scan up to left, above to right etc.
    """

    def __init__(self, msg):
        self.msg = msg


class OutputPassedToPreview(Exception):
    """ """

    def __init__(self, msg):
        self.msg = msg


class ReversedExcelRefError(Exception):
    """
    Raised where a user has provided an excel reference in a reversed format.

    Example:
    C5:A2
    """

    def __init__(
        self,
        msg=(
            "Invalid excel reference format. Please provide your reference in the "
            "standard upmost left to downmost right format, i.e A1:C5 not C5:A1"
        ),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


class UnknownDirectionError(Exception):
    """
    User has passed in a direction that is not a valid direction
    """

    def __init__(
        self,
        msg=("Direction is not a valid direction."),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


class IncorrectAssertionError(Exception):
    """
    Raised where a user is trying to define assertions for
    the assert_selections() method but has passed in
    invalid parameters.
    """

    def __init__(self, msg):
        self.msg = msg