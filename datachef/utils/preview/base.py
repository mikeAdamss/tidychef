from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List

from datachef.selection.selectable import Selectable


@dataclass
class BasePreview(metaclass=ABCMeta):
    @abstractmethod
    def print(selections: List[Selectable], to_path: Path = None, bound_selection=None): #pragma: no cover
        """
        An inline print of whatever this preview is previewing
        """
        ...

    @abstractmethod
    def _to_path(self, path: Path): #pragma: no cover
        """
        The mechanism to push whatever this is previewing to
        a filepath.
        """
        ...
