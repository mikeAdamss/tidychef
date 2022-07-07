from dataclasses import dataclass
from typing import Union

from datachef.models.dsd.components.base import BaseComponent
from datachef.models.source.cell import Cell, VirtualCell
from datachef.selection.selectable import Selectable
from datachef.lookup.engines.direct import Directly
from datachef.cardinal.directions import Direction

@dataclass
class ComponentDimensionConstant(BaseComponent):
    """
    Represents a dimension with a single constant value
    """

    name: str
    constant: Union[str, VirtualCell] = None

    _post_init_ran: bool = False

    def _post_init(self):
        """
        Create a virtual cell to hold the constant so we can
        compare like to like and track provenance information
        """
        self.constant = VirtualCell(value=self.constant)
        self._post_init_ran = True

    def resolve(self, _: Cell = None) -> VirtualCell:
        """
        Resolve the value of an observation against
        this component.

        It's a constant so it doesn't matter what
        source cell is asking.
        """

        if not self._post_init_ran:
            self._post_init()

        return self.constant


@dataclass
class ComponentDimensionDirect(BaseComponent):
    """
    Represents a dimension created from a single visual relationship
    """

    name: str
    selection: Selectable
    engine: Directly
    direction: Direction

    _post_init_ran: bool = False


    def _post_init(self):
        """
        Instantiate the engine class so we can resolve
        this dimension relative to any observation.
        """
        
        self.engine = self.engine(self.selection, self.direction)
        self._post_init_ran = True


    def resolve(self, ob_cell: Cell) -> Cell:
        """
        Resolve the value of an observation using
        a direct relationship to this dimension.
        """

        if not self._post_init_ran:
            self._post_init()

        return self.engine.resolve(ob_cell)