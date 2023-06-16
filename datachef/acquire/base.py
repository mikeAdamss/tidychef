"""
Holds the definition of the reader baseclass: BaseReader

The BaseReader is to provide functionality that is standard to all readers.
"""

from abc import ABCMeta, abstractmethod, abstractstaticmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from datachef.exceptions import FileInputError
from datachef.selection.selectable import Selectable


@dataclass
class BaseReader(metaclass=ABCMeta):
    """
    Baseclass that all readers inherit from.
    """

    @abstractmethod
    def parse(self) -> Selectable:
        """Parse the datasource into a selectable thing"""

