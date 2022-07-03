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


class ComponentConstructionError(Exception):
    """
    Raised where a user has passed bad or invalid parameters
    into a component costructor.
    """

    def __init__(
        self,
        msg=("Invalid parameters supplied to constructor."),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


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


class UnsupportedLocalFileError(Exception):
    """
    User has passed in a local file of a type not currently supported.
    """

    def __init__(
        self,
        msg=("Provided file type is not supported."),
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
