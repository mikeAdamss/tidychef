import pytest

from datachef.models.dsd.components.dimension import (
    Dimension, ComponentDimensionConstant
)


def test_dimension_constant_constructor():
    """
    Test that where appropriate minimum params are supplied a dimension
    of type DimensionConstant is created
    """

    dimension = Dimension("A constant dimension", constant="foo")
    assert isinstance(dimension.component, ComponentDimensionConstant), (
        f"Expecting dimension type {ComponentDimensionConstant}"
        f", for {dimension.component}"
    )
    
    dimension.component._post_init() # Does nothing for constants, just for coverage
    resolved = dimension.component.resolve()
    assert resolved == 'foo', f'Expecting "foo", got {resolved}'


def test_failed_construction_repr():
    """
    Test that where an issue is encoutered constructing the component
    we get the expected feedback.
    """

    with pytest.raises(Dimension.contextual_exception) as err_info:
        Dimension("Nothing uses only one arg")
