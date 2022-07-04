from datachef.exceptions import BadDimensionConstructor
from datachef.models.dsd.components.base import ComponentMatcher

from ..base import ComponentVariant
from .variants import ComponentDimensionConstant


class Dimension(ComponentMatcher):
    """
    A constructor for selecting the appropriate dimension component.
    """

    contextual_exception = BadDimensionConstructor
    inventory = [
        ComponentVariant(
            component_class=ComponentDimensionConstant,
            arg_types=[str],
            required_kwargs=["constant"],
        )
    ]
