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
