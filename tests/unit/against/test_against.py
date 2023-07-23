import pytest

from datachef import against
from datachef.against.implementations.items import ItemsValidator
from datachef.against.implementations.length import LengthValidator
from datachef.against.implementations.numeric import (
    IsNotNumericOrFloatValidator,
    IsNotNumericValidator,
    IsNumericOrFloatValidator,
    IsNumericValidator,
)
from datachef.against.implementations.regex import RegexValidator
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


def test_against_is_numeric():
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


def test_against_is_numeric_or_float():
    """
    Test that validating against numeric works
    """

    validator = against.is_numeric_or_float
    assert isinstance(validator, IsNumericOrFloatValidator)

    # Not valid
    cell = Cell(x="0", y="0", value="baz")
    assert validator(cell) is False

    # Test message generator small message with list output
    assert validator.msg(cell) == '"baz" is not numeric or a float'

    # Is Valid
    cell = Cell(x="0", y="0", value="1.6")
    assert validator(cell) is True

    # Confirm we dont get fooled by pre and post .'s
    cell = Cell(x="0", y="0", value=".1")
    assert validator(cell) is False

    # Confirm we dont get fooled by pre and post .'s
    cell = Cell(x="0", y="0", value="1.")
    assert validator(cell) is False


def test_against_is_not_numeric():
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


def test_against_is_not_numeric_or_float():
    """
    Test that validating against non numeric works
    """

    validator = against.is_not_numeric_or_float
    assert isinstance(validator, IsNotNumericOrFloatValidator)

    # Not valid
    cell = Cell(x="0", y="0", value="1.1")
    assert validator(cell) is False

    # Test message generator small message with list output
    assert validator.msg(cell) == '"1.1" is numeric or a float'

    # Is Valid
    cell = Cell(x="0", y="0", value="baz")
    assert validator(cell) is True

    # Confirm we dont get fooled by pre and post .'s
    cell = Cell(x="0", y="0", value=".1")
    assert validator(cell) is True

    # Confirm we dont get fooled by pre and post .'s
    cell = Cell(x="0", y="0", value="1.")
    assert validator(cell) is True


def test_against_length():
    """
    Test we can validate cell values based on length
    """

    # Both least and most
    validator = against.length(least=2, most=5)
    assert isinstance(validator, LengthValidator)
    cell = Cell(x="0", y="0", value="aaa")
    assert validator(cell) is True
    cell = Cell(x="0", y="0", value="aaaaaa")
    assert validator(cell) is False
    assert (
        validator.msg(cell)
        == 'The length of cell value "aaaaaa" is not between 2 and 5 in length.'
    )

    # most
    validator = against.length(most=5)
    assert isinstance(validator, LengthValidator)
    cell = Cell(x="0", y="0", value="a")
    assert validator(cell) is True
    cell = Cell(x="0", y="0", value="aaaaaa")
    assert validator(cell) is False
    assert (
        validator.msg(cell)
        == f'The length of cell value "aaaaaa" is not below the maximum length of 5.'
    )

    # least
    validator = against.length(least=2)
    assert isinstance(validator, LengthValidator)
    cell = Cell(x="0", y="0", value="aaaaaa")
    assert validator(cell) is True
    cell = Cell(x="0", y="0", value="a")
    assert validator(cell) is False
    assert (
        validator.msg(cell)
        == 'The length of cell value "a" is not above the minimum length of 2.'
    )

    with pytest.raises(AssertionError):
        against.length(least=20, most=10)

    with pytest.raises(AssertionError):
        against.length()
