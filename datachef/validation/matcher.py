import re
from typing import Optional

from datachef.exceptions import NoMatcherSpecifiedError
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
        self.match_regex: bool = False
        self.regex_pattern: Optional[str] = None

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
        try:
            if self.match_regex:
                self.__regex_implemented(cell)
            else:
                # Catch and help any users calling with configuring
                raise NoMatcherSpecifiedError()
        except NoMatcherSpecifiedError as err:
            raise err
        except Exception as err:
            if self.print_not_raise_exception:
                print(str(err))
            else:
                raise err

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
