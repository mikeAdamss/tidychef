import copy
from functools import wraps


def dontmutate(method):
    """
    Decorates a method so that where returning self
    any operations are made on a _copy_ of self.

    Without this, the following patterns:

    selection2 = selection1.do_something()
    or
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
