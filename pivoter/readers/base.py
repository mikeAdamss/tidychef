from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseReader(metaclass=ABCMeta):
    source: Any

    @abstractmethod
    def parse(self):
        ...
