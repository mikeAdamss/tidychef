from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from datachef.selection.selectable import Selectable

@dataclass
class BaseReader(metaclass=ABCMeta):
    """
    Baseclass that all readers inherit from.
    """

    # Note - we attach tables to the reader for a reason.
    # Some (but not all) table reading libraries allow you
    # to only read in certain sheets (rather than our default
    # of filtering out after reading).
    # Where this is possible this allows us to hand the filtering
    # of tables names over to the reader (which can then None this
    # property).
    tables: Optional[str] = None

    @abstractmethod
    def parse(
        self, source: Any, selectable: Selectable, **kwargs
    ) -> Union[Selectable, List[Selectable]]:
        """Parse the datasource into a selectable thing"""
