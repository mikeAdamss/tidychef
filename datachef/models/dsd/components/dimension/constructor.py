from datachef.exceptions import BadDimensionConstructor

from .variants import ComponentDimensionConstant

from datachef.models.dsd.components.base import ComponentFactory

from ..base import ComponentVariant


class Dimension(ComponentFactory):
    """
    A constructor for selecting the appropriate dimension component.
    """

    contextual_exception = BadDimensionConstructor
    inventory = [
        ComponentVariant(
            component_class = ComponentDimensionConstant,
            arg_types = [str],
            required_kwargs = ["constant"]
            )
    ]
