from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from pivoter.selection.base import Selectable


@dataclass
class BasePreview(metaclass=ABCMeta):

    selectable: Selectable

    @abstractmethod
    def print(self, to_path: Path = None):
        """
        An inline print of whatever this preview is previewing
        """
        ...

    @abstractmethod
    def _to_path(self, path: Path):
        """
        The mechanism to push whatever this is previewing to
        a filepath.
        """
        ...
