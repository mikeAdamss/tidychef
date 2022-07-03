"""
Base class for all DSD components
"""

from abc import ABCMeta
from dataclasses import dataclass
from typing import Any, Optional

from datachef.engines.base import BaseEngine
from datachef.exceptions import ComponentConstructionError


@dataclass
class BaseComponent(metaclass=ABCMeta):
    """
    The shared basic definition of a component

    :param constant: if this component is a constant against
    each observation, this holds the value of that constant.
    """

    name: Optional[str]
    relational_engine: Optional[BaseEngine]
    engine_param1: Optional[Any]
    engine_param2: Optional[Any]
    constant: Optional[str]

    def validate(self):
        if self.constant and self.relational_engine:
            ComponentConstructionError(
                "A component can either be set with a constant or can have "
                "an engine specified for unpicking the visual relationship. "
                "It should never have both"
            )
