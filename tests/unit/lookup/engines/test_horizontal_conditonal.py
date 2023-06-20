import pytest

from datachef.column.column import Column
from datachef.exceptions import (
    BadConditionalResolverError,
    HorizontalConditionalHeaderError,
)
from datachef.lookup.engines.horizontal_condition import HorizontalCondition


def test_horizontal_resolver_exceptions():
    """
    Test the horizontal resolver exceptions are raised as
    expected.
    """

    # Resolver returning wrong type
    with pytest.raises(BadConditionalResolverError):
        horizontal_conditional = HorizontalCondition("", resolver=lambda x: 6)
        horizontal_conditional.resolve("", {"foo": "fooval", "bar": "barval"})

    # Resolver passed a non dict type
    with pytest.raises(BadConditionalResolverError):
        horizontal_conditional = HorizontalCondition(
            "", resolver=lambda x: x["foo"] + x["bar"]
        )
        horizontal_conditional.resolve("", True)

    # Resolver passed a dict of not pure strings
    with pytest.raises(BadConditionalResolverError):
        horizontal_conditional = HorizontalCondition(
            "", resolver=lambda x: x["foo"] + x["bar"]
        )
        horizontal_conditional.resolve("", {"foo": 6.5, "bar": False})


def test_single_horizontal_conditional():
    """
    Test a single simple horizontal conditional
    """

    horizontal_conditional = HorizontalCondition(
        "", resolver=lambda x: x["foo"] + x["bar"]
    )

    resolved = horizontal_conditional.resolve("", {"foo": "fooval", "bar": "barval"})
    assert resolved == "foovalbarval"


def test_single_horizontal_conditional_raises_for_missing_key():
    """
    Test a single simple horizontal conditional
    """

    horizontal_conditional = HorizontalCondition(
        "", resolver=lambda x: x["foo"] + x["bar"]
    )

    resolved = horizontal_conditional.resolve("", {"foo": "fooval", "bar": "barval"})
    assert resolved == "foovalbarval"


def test_horizontal_conditional_header_error_raises():
    """
    Test the exception HorizontalConditionalHeaderError
    is raised where expected.
    """

    # Expect a column of baz
    column = Column.horizontal_condition("", resolver=lambda x: x["baz"])

    # But provide no columns at all.
    with pytest.raises(HorizontalConditionalHeaderError):
        column.resolve_column_cell_from_obs_cell("", {})
