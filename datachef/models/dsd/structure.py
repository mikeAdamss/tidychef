from datachef.selection.selectable import Selectable


class Structure:
    """
    Principle constructor for forming components into
    a coherent output.
    """

    def __init__(self, *components, observations: Selectable = None):

        if not observations or not isinstance(observations, Selectable):
            ...
