class BadExcelReferenceError(Exception):
    """
    Raised where the user has provided an excel reference that does not match
    the known patterns for excel references.
    """

    def __init__(self, msg):
        self.msg = msg


class BadShiftParameterError(Exception):
    """
    Raised where someone has provided incorrect inputs to the
    shift method.
    """

    def __init__(self, msg):
        self.msg = msg


class CardinalDeclarationWithOffset(Exception):
    """
    User had tried to pass in an argument to a direction
    in a context where its just being used to declare an
    absolute cardinal direction.
    """

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
    """
    User it trying to call preview() with a TidyData class
    in place of Selectables
    """

    def __init__(self, msg):
        self.msg = msg


class ReversedExcelRefError(Exception):
    """
    Raised where a user has provided an excel reference in a reversed format.

    Example:
    C5:A2
    """

    def __init__(self, msg):
        self.msg = msg


class UnknownDirectionError(Exception):
    """
    User has passed in a direction that is not a valid direction
    """

    def __init__(self, msg):
        self.msg = msg


class ReferenceOutsideSelectionError(Exception):
    """
    User is trying to make a narrow selection of cells
    but has already filtered the cells in question out
    of the table via a prior action.
    """

    def __init__(self, msg):
        self.msg = msg


class AmbiguousWaffleError(Exception):
    """
    User is trying to use the waffle method but has
    provided invalid combinations of selections.
    """

    def __init__(self, msg):
        self.msg = msg
