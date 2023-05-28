import copy
from functools import wraps


def dontmutate(method):
    """
    Decorates a method so that any changes
    are made to a _copy_ of self not self.

    Without this, the following patterns:

    selection2 = selection1.do_something()

    match2 = match.regex("foo")

    Would change the value in the righthand
    classes (selection1 and match) as well
    as their lefthand assignations.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self = copy.deepcopy(self)
        return method(self, *args, **kwargs)

    return wrapper
