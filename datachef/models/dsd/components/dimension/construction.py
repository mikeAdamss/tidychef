from datachef.cardinal.directions import Direction
from datachef.exceptions import DimensionConstructionError
from datachef.lookup.engines.direct import Directly
from datachef.models.dsd.components.base import ComponentConstructor
from datachef.selection.selectable import Selectable

from ..base import ComponentVariant
from .variants import ComponentDimensionConstant, ComponentDimensionDirect


class Dimension(ComponentConstructor):
    """
    A constructor for selecting the appropriate dimension component.
    """

    contextual_exception = DimensionConstructionError
    inventory = [
        ComponentVariant(
            component_class=ComponentDimensionConstant,
            arg_types=[str],
            required_kwargs=["constant"],
        ),
        ComponentVariant(
            component_class=ComponentDimensionDirect,
            arg_types=[str, Selectable, Directly, Direction],
        ),
    ]
