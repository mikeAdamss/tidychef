import pytest

from datachef.exceptions import NoMatcherSpecifiedError
from datachef.models.source.cell import Cell
from datachef.validation import Matcher


def test_new_instances_do_not_mutate():
    """
    Test that when we select a matching strategy
    i.e .regex(), this correctly creates a new
    instance of Matcher, leaving the initial
    instance unchanged.
    """

    matcher = Matcher()
    assert matcher.match_regex is False
    assert matcher.regex_pattern is None

    matcher2 = matcher.regex("foo")
    assert matcher2.match_regex is True
    assert matcher2.regex_pattern == "foo"

    assert matcher.match_regex is False
    assert matcher.regex_pattern is None


def test_regex_matcher():
    """
    Test the regex matching works
    """

    match = Matcher().regex("foo")

    # Should not error as the cell value it is a regex match
    matching_cell = Cell(value="foo")
    match(matching_cell)

    # Should error as its not
    non_matching_cell = Cell(value="donkeys")
    with pytest.raises(AssertionError):
        match(non_matching_cell)


def test_error_for_no_matches_specified():
    """
    Test that the expected Exception is raised
    where an observation is passed to a matcher
    before it has been configured.
    """

    match = Matcher()

    with pytest.raises(NoMatcherSpecifiedError):
        match("foo")


def test_errors_do_not_raise_specified():
    """
    Test that we can configure the matcher
    to print errors rather than raising them.
    """

    match = Matcher().regex("foo")

    # Should raise as "donkeys" != "foo"
    non_matching_cell = Cell(value="donkeys")
    with pytest.raises(AssertionError):
        match(non_matching_cell)

    # Should no longer raise
    match.print_not_raise_exception = True
    match(non_matching_cell)
