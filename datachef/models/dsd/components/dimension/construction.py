from datachef.exceptions import DimensionConstructionError
from datachef.models.dsd.components.base import ComponentConstructor

from ..base import ComponentVariant
from .variants import ComponentDimensionConstant, ComponentDimensionDirect
from datachef.selection.selectable import Selectable
from datachef.lookup.engines.direct import Directly
from datachef.cardinal.directions import Direction

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
            component_class = ComponentDimensionDirect,
            arg_types = [str, Selectable, Directly, Direction]
        )
    ]
