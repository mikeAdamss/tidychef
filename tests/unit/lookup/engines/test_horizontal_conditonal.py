import copy
from dataclasses import dataclass
from os import linesep

import pytest

from datachef.cardinal.directions import down, left, right, up
from datachef.exceptions import (
    FailedLookupError,
    MissingDirectLookupError,
    UnknownDirectionError,
)
from datachef.lookup.engines.horizontal_condition import HorizontalCondition
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.selection import filters
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_wide_band_tab
from datachef.exceptions import BadConditionalResolverError

def test_horizontal_resolver_exceptions():
    """
    Test the horizontal resolver exceptions are raised as
    expected.
    """

    # Resolver returning wrong type
    with pytest.raises(BadConditionalResolverError):
        horizontal_conditional = HorizontalCondition(
                    "",
                    resolver = lambda x: 6
                )
        horizontal_conditional.resolve("", {"foo": "fooval", "bar": "barval"})

    # Resolver passed a non dict type
    with pytest.raises(BadConditionalResolverError):
            horizontal_conditional = HorizontalCondition(
                    "",
                    resolver = lambda x: x["foo"]+x["bar"]
                )
            horizontal_conditional.resolve("", True)

    # Resolver passed a dict of not pure strings
    with pytest.raises(BadConditionalResolverError):
            horizontal_conditional = HorizontalCondition(
                    "",
                    resolver = lambda x: x["foo"]+x["bar"]
                )
            horizontal_conditional.resolve("", {"foo": 6.5, "bar": False})


def test_single_horizontal_conditional():
    """
    Test a single simple horizontal conditional
    """

    horizontal_conditional = HorizontalCondition(
        "",
        resolver = lambda x: x["foo"]+x["bar"]
    )

    resolved = horizontal_conditional.resolve("", {"foo": "fooval", "bar": "barval"})
    assert resolved == "foovalbarval"

