import re

from datachef.models.source.cell import Cell
from datachef.utils.decorators import dontmutate
from datachef.validation.base import BaseValidation


class Matcher(BaseValidation):
    """
    The standard Matcher used to provide validation
    of the data being extracted.

    Please note - all Matcher methods should operate
    against a single Cell at a time and throw an
    exception where a Cell does not match the expected.
    """

    def __init__(self):
        self.match_regex = False
        self.regex_pattern = None

    def _pristine(self):
        """
        Returns Matcher to a pristine state
        """
        return Matcher()

    def __call__(self, cell: Cell):
        """
        When called, apply whichever validation method
        is toggled on for this instance of Matcher
        """
        if self.match_regex:
            self.__regex_implemented(cell)
        else:
            # Catch and help any users calling with configuring
            raise Exception(
                f"""
                You are passing a cell to a Matcher that has not
                been configured with a matching strategy.

                Examples of correct usage:

                match.regex("foo")
                match.one_of("foo", "bar", "baz")
            """
            )

    # -----
    # regex
    # -----

    @dontmutate
    def regex(self, pattern: str):
        """
        Set up matcher to use regex matching
        """
        new_matcher = self._pristine()
        assert isinstance(
            pattern, str
        ), "The value passed into '.regex()' should be a string"
        new_matcher.regex_pattern = pattern
        new_matcher.match_regex = True
        return new_matcher

    def __regex_implemented(self, cell: Cell):
        """
        Actually do regex matching
        """
        assert re.match(
            self.regex_pattern, cell.value
        ), f'Value of cell "{cell}" does not match provided regex pattern "{self.regex_pattern}".'
