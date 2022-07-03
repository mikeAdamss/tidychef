"""
Base class for all DSD components
"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from datachef.exceptions import ComponentConstructionError
from datachef.lookup.base import BaseLookupEngine
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable


class BaseComponent(metaclass=ABCMeta):
    """
    The shared basic definition of a component
    """

    def __init__(self, name: str, *args, **kwargs):
        self.name: str = name
        self._post_init(*args, **kwargs)

    @abstractmethod
    def _post_init(self, *args, **kwargs):
        """
        Instantiation behavioud specific to
        the given subclass of BaseComponent
        """

    @abstractmethod
    def resolve(self, ob_cell: Cell = None):
        """
        Resolve the value of an observation against
        this component.
        """

    @abstractmethod
    def validate(self):
        """
        Validate that the component in question has
        bee instiantiated in a valid way
        """
