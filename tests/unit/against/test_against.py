import pytest

from datachef import against
from datachef.against.implementations.items import ItemsValidator
from datachef.against.implementations.regex import RegexValidator
from datachef.against.implementations.numeric import IsNotNumericValidator, IsNumericValidator
from datachef.models.source.cell import Cell


def test_against_regex():
    """
    Test that validating against regex works
    """

    validator = against.regex("foo")
    assert isinstance(validator, RegexValidator)

    # Not valid
    cell = Cell(x="0", y="0", value="bar")
    assert validator(cell) is False

    # Test message generator
    assert validator.msg(cell) == '"bar" does not match pattern: "foo"'

    # Is Valid
    validator = against.regex("bar")
    assert validator(cell) is True


def test_against_items():
    """
    Test that validating against a list of items works
    """

    validator = against.items(["foo", "bar"])
    assert isinstance(validator, ItemsValidator)

    # Not valid
    cell = Cell(x="0", y="0", value="baz")
    assert validator(cell) is False

    # Test message generator small message with list output
    assert '"baz" not in list: [' in validator.msg(cell)

    # Test message generator small messge
    validator = against.items(
        ["1", "2", "3", "4", "5", "6", "7" "8", "9", "10", "11", "12"]
    )
    assert validator.msg(cell) == '"baz" not in list.'

    # Is Valid
    validator = against.items(["foo", "bar", "baz"])
    assert validator(cell) is True


def test_is_numeric():
    """
    Test that validating against numeric works
    """

    validator = against.is_numeric
    assert isinstance(validator, IsNumericValidator)

    # Not valid
    cell = Cell(x="0", y="0", value="baz")
    assert validator(cell) is False

    # Test message generator small message with list output
    assert validator.msg(cell) == '"baz" is not numeric'

    # Is Valid
    cell = Cell(x="0", y="0", value="1")
    assert validator(cell) is True

def test_is_not_numeric():
    """
    Test that validating against non numeric works
    """

    validator = against.is_not_numeric
    assert isinstance(validator, IsNotNumericValidator)

    # Not valid
    cell = Cell(x="0", y="0", value="1")
    assert validator(cell) is False

    # Test message generator small message with list output
    assert validator.msg(cell) == '"1" is numeric'

    # Is Valid
    cell = Cell(x="0", y="0", value="baz")
    assert validator(cell) is True