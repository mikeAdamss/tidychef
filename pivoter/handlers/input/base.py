from abc import ABCMeta, abstractmethod
from typing import Any

import pivoter.models.source.input


class BaseInputHandler(metaclass=ABCMeta):
    source: Any

    @abstractmethod
    def parse(self) -> pivoter.models.source.input.Input:
        ...
