import copy
from functools import wraps


def dontmutate(method):
    """
    Decorates a method so that where returning self
    any operations are made on a _copy_ of self.

    Without this, the following pattern:
    f2 = f1.do_something()

    Would change the value of f1 as well as assigning
    said new value to f2.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self = copy.deepcopy(self)
        return method(self, *args, **kwargs)

    return wrapper
