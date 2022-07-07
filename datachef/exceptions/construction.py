class ComponentConstructionError(Exception):
    """Base class for component construciton errors"""

    ...


class DimensionConstructionError(ComponentConstructionError):
    """
    User has passed in a bad combination of params to a dimension constructor.
    """

    def __init__(
        self,
        msg=(
            "Cannot construct dimension, an unrecognised combination of parameters has been supplied."
        ),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)
