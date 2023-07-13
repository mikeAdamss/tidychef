from abc import ABCMeta, abstractmethod
from typing import Any, List, Union

from datachef.selection.selectable import Selectable


class BaseReader(metaclass=ABCMeta):
    """
    Baseclass that all readers inherit from.
    """

    @abstractmethod
    def parse(
        self, source: Any, selectable: Selectable, **kwargs
    ) -> Union[Selectable, List[Selectable]]:
        """Parse the datasource into a selectable thing"""
