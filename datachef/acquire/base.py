"""
Holds the definition of the reader baseclass: BaseReader

The BaseReader is to provide functionality that is standard to all readers.
"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from datachef.selection.selectable import Selectable


@dataclass
class BaseReader(metaclass=ABCMeta):
    """
    Baseclass that all readers inherit from.
    """

    @abstractmethod
    def parse(self) -> Selectable:
        """Parse the datasource into a selectable thing"""
