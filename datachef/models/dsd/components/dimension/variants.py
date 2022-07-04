from dataclasses import dataclass

from datachef.models.dsd.components.base import BaseComponent
from datachef.models.source.cell import Cell


@dataclass
class ComponentDimensionConstant(BaseComponent):
    """
    A dimension representing a constant value
    """

    name: str
    constant: str = None

    def _post_init(self, *args, **kwargs):
        """
        Required but not applicable in the case
        of constants
        """
        ...

    def resolve(self, ob_cell: Cell = None):
        """
        Resolve the value of an observation against
        this component.
        """
        return self.constant
