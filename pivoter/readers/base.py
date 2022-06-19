from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pivoter.exceptions import FileInputError
from pivoter.selection.base import Selectable


@dataclass
class BaseReader(metaclass=ABCMeta):
    source: Any

    def _raise_if_source_is_not_path(self):
        """
        Raise if the source is no a Path object.
        """
        if not isinstance(self.source, Path):
            raise FileInputError("The source needs to be pathlib.Path object")

    @abstractmethod
    def parse(self) -> Selectable:
        """Parse the datasource into a selectable thing"""
