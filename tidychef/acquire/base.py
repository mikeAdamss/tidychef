from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from tidychef.selection.selectable import Selectable


@dataclass
class BaseReader(metaclass=ABCMeta):
    """
    Baseclass that all readers inherit from.
    """

    tables: Optional[str] = None

    @abstractmethod
    def parse(
        self, source: Any, selectable: Selectable, **kwargs
    ) -> Union[Selectable, List[Selectable]]:
        """Parse the datasource into a selectable thing"""
