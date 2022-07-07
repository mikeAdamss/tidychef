class NonExistentCellComparissonError(Exception):
    """
    User is trying to to make a positional comparison between an
    existant cell (i.e a cell parsed from a tabulated source) and
    a virtual cell created by a constant or other external input.
    """

    def __init__(
        self,
        msg=(
            "You cannot make a postitional comparisson between a cell parsed from a source input and a virtual cell."
        ),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


class InvlaidCellPositionError(Exception):
    """
    Raised where a cell has a value for one positional index but no the other.

    Examples:
    y has a value but x does not
    x has a value but y does not
    """

    def __init__(
        self,
        msg=("A cell with any postional values must exist on both the x and y axis."),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)
