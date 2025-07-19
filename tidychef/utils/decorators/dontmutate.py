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
    
    This optimized version uses shallow copy for most attributes
    and only deep copies the cells list and filtered table data,
    while preserving references to expensive indices.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Since self is always a Selectable, we can optimize specifically for it
        new_self = copy.copy(self)
        
        # Only copy the cells list (shallow copy - just the list, not the cell objects)
        # Everything else can be shared since indices are read-only
        if hasattr(self, 'cells') and self.cells is not None:
            new_self.cells = self.cells.copy()
        
        # If there's a filtered table, copy its cells list too
        if hasattr(self, 'filtered') and self.filtered is not None and hasattr(self.filtered, 'cells'):
            if self.filtered.cells is not None:
                new_self.filtered = copy.copy(self.filtered)
                new_self.filtered.cells = self.filtered.cells.copy()
        
        return method(new_self, *args, **kwargs)

    return wrapper
