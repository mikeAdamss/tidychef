"""
Base class for all DSD components
"""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseComponent(metaclass=ABCMeta):

    # see: pivoter/hints
    hints: bool = False

    def _trigger_hints(self):
        """
        Whether to trigger the HINT level logging statments for this component
        """
        if self.hints:
            self.hints()

    def hints(self):
        """
        Generates HINT level logging statments for this component.

        To be overwritten per component class if hints are implemented.
        """
        ...

    @abstractmethod
    def get_help_str(self) -> str:
        """
        An explanation of what this component is and what it is used for.
        """
        ...
